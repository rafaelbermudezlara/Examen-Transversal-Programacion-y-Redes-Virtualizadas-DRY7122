# =============================================================================
# Ítem 3: Gestión de Usuarios con Contraseñas Hash y SQLite
# Este script crea un servicio web simple para registrar y validar usuarios
# almacenando sus contraseñas en formato hash en una base de datos SQLite.
# =============================================================================

# Paso 1: Tener los códigos requeridos que permita importar la gestión de claves y el uso de base de datos SQL.
# Importación de librerías esenciales
import sqlite3    # Para la gestión de la base de datos SQLite
import hashlib    # Para generar hashes de contraseñas (gestión de claves)
from flask import Flask, request # Para crear el servicio web

# Importaciones adicionales del laboratorio original (pyotp, uuid) que pueden no ser directamente
# usadas en este ítem específico pero son parte del contexto del laboratorio de seguridad.
import pyotp # Para contraseñas de un solo uso (One-Time Passwords)
import uuid  # Para generar identificadores únicos (Universally Unique Identifiers)


app = Flask(__name__)
db_name = 'examen.db' # Nombre de la base de datos SQLite que se creará en el mismo directorio del script

# =============================================================================
# Paso 2: Debe tener los códigos necesarios que permita al archivo crear el sitio web,
# el cual utilizará el puerto 7500.
# =============================================================================

@app.route('/')
def index():
    """
    Ruta raíz del servicio web. Muestra un mensaje de bienvenida.
    """
    return 'Bienvenido al laboratorio práctico para una evolución de los sistemas de contraseñas!'


# =============================================================================
# Paso 3: Ingresar los códigos respectivos para almacenar usuarios y contraseñas en hash.
# =============================================================================

@app.route('/signup/v2', methods=['GET', 'POST'])
def signup_v2():
    """
    Permite el registro de nuevos usuarios, almacenando la contraseña en formato hash SHA256.
    La tabla USER_HASH se crea si no existe.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Crea la tabla USER_HASH si no existe. USERNAME es la clave primaria.
    c.execute("""CREATE TABLE IF NOT EXISTS USER_HASH
               (USERNAME TEXT PRIMARY KEY NOT NULL,
                HASH TEXT NOT NULL); """)
    conn.commit()

    try:
        # Codifica la contraseña a bytes y luego calcula su hash SHA256, obteniendo el resultado en hexadecimal.
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
        # Inserta el nombre de usuario y el hash de la contraseña en la tabla.
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH)"
                  " VALUES ('{0}', '{1}')".format(request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        # Maneja el caso en que el nombre de usuario ya existe (debido a PRIMARY KEY NOT NULL).
        conn.close()
        return "el usuario ha sido registrado"
    
    # Imprime la información en la consola del servidor (para depuración).
    print('nombre de usuario: ', request.form['username'], ' contraseña: ', request.form['password'], ' hash: ', hash_value)
    conn.close()
    return "registro exitoso"


# =============================================================================
# Paso 4: A través de comando respectivo, validará los usuarios, que en este caso
# serán los nombres de los integrantes el examen, las contraseñas a utilizar será a elección.
# =============================================================================

def verify_hash(username, password):
    """
    Verifica si la contraseña proporcionada coincide con el hash almacenado para un usuario.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Consulta el hash de la contraseña para el usuario dado.
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone() # Obtiene la primera (y única) fila de resultado.
    conn.close()

    # --- INICIO DE LÍNEAS DE DEPURACIÓN ---
    print(f"DEBUG: Intento de login para usuario: {username}")
    if records:
        print(f"DEBUG: Hash almacenado en DB para '{username}': {records[0]}")
    else:
        print(f"DEBUG: Usuario '{username}' NO encontrado en la base de datos.")

    computed_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"DEBUG: Hash calculado de la contraseña ingresada: {computed_hash}")
    # --- FIN DE LÍNEAS DE DEPURACIÓN ---

    if not records:
        return False
    
    # Esta es la comparación clave
    if records[0] == computed_hash:
        print("DEBUG: ¡Los hashes COINCIDEN! Inicio de sesión exitoso.")
        return True
    else:
        print("DEBUG: Los hashes NO COINCIDEN. Inicio de sesión fallido.")
        return False

@app.route('/login/v2', methods=['GET', 'POST'])
def login_v2():
    """
    Permite el inicio de sesión de usuarios, verificando la contraseña hasheada.
    """
    # --- AÑADIDA LÍNEA DE DEPURACIÓN ---
    print("DEBUG: ¡La solicitud /login/v2 ha llegado a la función!")
    # ----------------------------------
    error = None
    if request.method == 'POST':
        # Intenta verificar las credenciales usando la función verify_hash.
        if verify_hash(request.form['username'], request.form['password']):
            error = 'inicio de sesión exitoso'
        else:
            error = 'Usuario/contraseña inválidos'
    else:
        error = 'Método no válido' # Para solicitudes GET a esta ruta.
    return error

# =============================================================================
# Bloque principal para ejecutar la aplicación Flask
# Esto inicia el servidor web en el puerto 7500.
# =============================================================================
if __name__ == '__main__':
    # Se ejecuta la aplicación Flask en el host 0.0.0.0 (accesible desde cualquier IP)
    # y en el puerto 7500, utilizando un contexto SSL ad-hoc para HTTPS.
    app.run(host='0.0.0.0', port=7500, ssl_context='adhoc')


