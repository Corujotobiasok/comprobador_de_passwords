COMPROBADOR DE CONTRASEÑAS - GUÍA DE USO

¡Bienvenido al proyecto Comprobador de Contraseñas!

Este repositorio permite a los usuarios verificar si su contraseña aparece en la conocida base de datos rockyou.txt, utilizada en pruebas de seguridad y por hackers. Es una herramienta educativa para ayudarte a mejorar la seguridad de tus contraseñas.

CONTENIDO DEL REPOSITORIO:

1. app.py               -> Código principal en Python usando Flask.
2. templates/            -> Carpeta que contiene los archivos HTML para la interfaz web.
   - index.html          -> Página principal del sitio web.
3. passwords.txt         -> Lista opcional de contraseñas (si quieres usar tu propia lista).

REQUISITOS:

- Python 3.8 o superior
- Flask
- Navegador web para acceder a la interfaz
- Opcional: archivo de contraseñas personalizado (.txt)

INSTALACIÓN:

1. Clona o descarga este repositorio.
2. Abre la terminal y navega a la carpeta del proyecto.
3. Crea un entorno virtual (opcional pero recomendado):
   - Windows: python -m venv venv
   - Linux/Mac: python3 -m venv venv
4. Activa el entorno virtual:
   - Windows: venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate
5. Instala Flask:
   pip install Flask

USO:

1. Coloca el archivo 'passwords.txt' en la carpeta raíz del proyecto, si no quieres usar el archivo predeterminado.
2. Ejecuta la aplicación:
   python app.py
3. Abre tu navegador y visita:
   http://127.0.0.1:5000
4. Ingresa tu contraseña en el formulario y haz clic en "Analizar".
5. La aplicación te mostrará si tu contraseña aparece en el archivo rockyou.txt y te dará recomendaciones de seguridad.

FUNCIONES ADICIONALES:

- Botón para mostrar u ocultar la contraseña mientras la escribes.
- Mensajes claros indicando si la contraseña es segura o vulnerable.
- No se guarda ninguna contraseña en el servidor, todo se procesa temporalmente en memoria.

RECOMENDACIONES DE SEGURIDAD:

- No uses contraseñas reales de cuentas críticas mi
