from flask import Flask, render_template, request, redirect, session
import sqlite3, bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Crear base de datos si no existe
conn = sqlite3.connect("usuarios.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
conn.commit()
conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    user = request.form["username"]
    pw = request.form["password"].encode("utf-8")
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())

    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (user, hashed))
        conn.commit()
    except:
        return "Usuario ya existe"
    finally:
        conn.close()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pw = request.form["password"].encode("utf-8")

    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT password FROM usuarios WHERE username=?", (user,))
    row = c.fetchone()
    conn.close()

    if row and bcrypt.checkpw(pw, row[0]):
        session["usuario"] = user
        return f"Bienvenido {user}"
    else:
        return "Usuario o contraseña incorrecta"

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)