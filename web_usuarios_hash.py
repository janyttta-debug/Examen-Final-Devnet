from flask import Flask
import sqlite3
import hashlib

app = Flask(__name__)

def crear_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    usuarios = [
        ("MArtina Quintana", "Prueba123"),
        ("Alejandra Quintana", "Prueba123")
    ]

    for usuario, password in usuarios:
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("""
        INSERT INTO usuarios (usuario, password_hash)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM usuarios WHERE usuario = ?
        )
        """, (usuario, password_hash, usuario))

    conexion.commit()
    conexion.close()

@app.route("/")
def inicio():
    return """
    <h1>Sitio Web Puerto 5800</h1>
    <p>Base de datos SQLite creada correctamente.</p>
    <p>Usuarios almacenados con contraseña en hash.</p>
    """

@app.route("/usuarios")
def mostrar_usuarios():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, usuario, password_hash FROM usuarios")
    datos = cursor.fetchall()
    conexion.close()

    html = "<h1>Usuarios registrados</h1>"
    html += "<table border='1'>"
    html += "<tr><th>ID</th><th>Usuario</th><th>Password Hash</th></tr>"

    for fila in datos:
        html += f"<tr><td>{fila[0]}</td><td>{fila[1]}</td><td>{fila[2]}</td></tr>"

    html += "</table>"
    return html

if __name__ == "__main__":
    crear_base_datos()
    app.run(host="0.0.0.0", port=5800)
