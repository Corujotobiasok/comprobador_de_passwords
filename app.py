import os
from flask import Flask, render_template, request, redirect, url_for, flash

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PASSWORD_FILE = os.path.join(APP_DIR, "passwords.txt")

# Umbral para cargar en memoria (ajusta si quieres)
LOAD_THRESHOLD_BYTES = 50 * 1024 * 1024  # 50 MB

app = Flask(__name__)
app.secret_key = "cambia-esto-por-una-clave-secreta-en-produccion"  # solo dev

# Intentamos cargar el archivo en memoria si es pequeño (mejor rendimiento)
PASSWORD_SET = None
def try_load_password_set():
    global PASSWORD_SET
    if not os.path.exists(PASSWORD_FILE):
        PASSWORD_SET = None
        return False
    size = os.path.getsize(PASSWORD_FILE)
    if size > LOAD_THRESHOLD_BYTES:
        PASSWORD_SET = None
        return False
    s = set()
    with open(PASSWORD_FILE, "rb") as f:
        for raw in f:
            # decodificar con fallback seguro
            try:
                line = raw.decode("utf-8", errors="replace").strip()
            except Exception:
                line = raw.decode("latin-1", errors="replace").strip()
            if line:
                s.add(line)
    PASSWORD_SET = s
    return True

def stream_check_password(target):
    """Busca target en passwords.txt en modo streaming (no carga todo)."""
    if not os.path.exists(PASSWORD_FILE):
        return False
    t = target.strip()
    with open(PASSWORD_FILE, "rb") as f:
        for raw in f:
            try:
                line = raw.decode("utf-8", errors="replace").strip()
            except Exception:
                line = raw.decode("latin-1", errors="replace").strip()
            if line == t:
                return True
    return False

# Cargar al inicio si procede
try_load_password_set()

# Texto descriptivo sobre rockyou
ROCKYOU_DESC = (
    "Este repositorio contiene la popular lista de palabras rockyou.txt. "
    "Este archivo es un recurso ampliamente utilizado en la comunidad de ciberseguridad, "
    "especialmente para desafíos de Capture The Flag (CTF) y ejercicios de pruebas de penetración. "
    "Originalmente filtrado por una brecha de datos a gran escala de la empresa RockYou en 2009, "
    "el archivo rockyou.txt contiene millones de contraseñas comunes, lo que lo convierte en una "
    "herramienta esencial para el descifrado de contraseñas y las pruebas de seguridad."
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None  # 'vulnerable' or 'no_vulnerable' or None
    shown_password = None
    source = None
    details = None
    if request.method == "POST":
        # recibimos la contraseña en memoria; NO la guardamos en disco ni en logs
        pw = request.form.get("password", "")
        if not pw:
            flash("Ingresa una contraseña.", "error")
            return redirect(url_for("index"))

        try:
            if PASSWORD_SET is not None:
                found = pw in PASSWORD_SET
                source = "Archivo cargado en memoria"
            else:
                found = stream_check_password(pw)
                source = f"Archivo local: passwords.txt (streaming)" if os.path.exists(PASSWORD_FILE) else "Archivo no encontrado"
        except Exception:
            found = False
            source = "Error al procesar"
            details = "Se produjo un error al buscar la contraseña."

        if found:
            result = "vulnerable"
            # mostramos la contraseña solo en la respuesta actual (no persistimos)
            shown_password = pw
            details = details or "La contraseña coincide exactamente con una línea en el archivo."
        else:
            result = "no_vulnerable"
            details = details or "La contraseña no fue encontrada en el archivo."

        # renderizamos con la contraseña mostrada según pediste
        return render_template(
            "index.html",
            result=result,
            password=shown_password,
            source=source,
            details=details,
            rockyou_desc=ROCKYOU_DESC
        )

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
