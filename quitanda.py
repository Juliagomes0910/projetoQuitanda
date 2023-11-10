from flask import Flask, render_template, request, redirect, session 
import sqlite3 as sql
import uuid 

app= Flask(__name__)
app.secret_key = "quitandazezinho"

usuario = "jubs"
senha = "09102006"
login = False

#Função para a sessão 
def verifica_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False
    
#Conexao com o banco de dados
def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao

#Iniciar Banco de dados
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()

#Rota da página inicial 
@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database()
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    title = "Home"
    return render_template("home.html", produtos=produtos, title=title)

#ROTA DA PÁGINA LOGIN
@app.route("/login")
def login():
    title ="Login"
    return render_template("login.html",title=title)

#Rota da página incial 
@app.route("/acesso", methods=['post'])
def acesso():
    global usuario, senha 
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]
    if usuario== usuario_informado and senha == senha_informada:
        session["login"] = True 
        return redirect('/adm')
    else:
        return render_template("login.html", msg = "Usuário/Senha estão incorretos!")

#Rota da página adm
@app.route("/adm")
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        produtos = conexao.execute('SELECT * FRO  produtos ORDER BY id_prod DESC').fetchall()
        conexao.close()
        title = "Administração"
        return render_template("adm.html", produtos=produtos , title=title)
    else:
        return redirect("/login")





#Final do código 
app.run(debug=True)