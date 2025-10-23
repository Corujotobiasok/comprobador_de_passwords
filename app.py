# api/index.py
"""
Flask app minimalista que verifica si una contraseña está en passwords.txt
adaptada para funcionar en Vercel Serverless.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from vercel import Vercel  # necesario para serverless

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PASSWORD_FILE = os.path.join(APP_DIR, "passwords.txt")

LOAD_THRESHOLD_BYTES = 50 * 1024 * 1024  # 50 MB

app = Flask(__name__)
app.secret_key = "cambia-esto-por-una-clave-secreta-en-produccion"

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
            try:
                line = raw.decode("utf-8", errors="replace").strip()
            except Exception:
                line = raw.decode("latin-1", errors="replace").strip()
            if line:
                s.add(line)
    PASSWORD_SET = s
    return True

def stream_check_password(target):
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

try_load_password_set()

ROCKYOU_DESC = (
    "Este repositorio contiene la popular lista de palabras rockyou.txt. "
    "Archivo ampliamente utilizado en la comunidad de ciberseguridad para ejercicios CTF."
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    shown_password = None
    source = None
    details = None
    if request.method == "POST":
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
            shown_password = pw
            details = details or "La contraseña coincide exactamente con una línea en el archivo."
        else:
            result = "no_vulnerable"
            details = details or "La contraseña no fue encontrada en el archivo."

        return render_template(
            "index.html",
            result=result,
            password=shown_password,
            source=source,
            details=details,
            rockyou_desc=ROCKYOU_DESC
        )

    return render_template("index.html", result=None)

# Adaptación serverless para Vercel
handler = Vercel(app)
