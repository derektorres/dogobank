from flask import Flask, render_template, request, jsonify, redirect, url_for
from entities.user import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from entities.account import Account
from entities.log import Log
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/welcome')
@login_required
def welcome():
    account = Account.get_account_by_user(current_user.id)
    return render_template('welcome.html', account=account)

@app.route('/api/users', methods=["POST"])
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if User.check_email_exists(email):
        return jsonify({"success": False, "message": "El correo electrónico ingresado ya se encuentra registrado."}), 409

    new_user_id = User.save(name, email, password)

    if new_user_id:
        Log.save_log(id_user=new_user_id, description="creacion de cuenta exitoso", type= 2)
        return jsonify({"success": True, "message": "Su cuenta fue creada correctamente."}), 201
    else:
        return jsonify({"success": False, "message": "Ocurrió un error al crear su cuenta. Intente de nuevo"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)
    if user:
        if user.is_active == 1:
            login_user(user)
            Log.save_log(id_user=user.id, description="Inicio de sesión exitoso", type= 1)
            return jsonify({
                "success": True,
                "message": "Sesion Iniciada Correctamente"  
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "El perfil esta desactivado"
            })
    else:
        return jsonify({
            "success": False,
            "message": "Los datos dea cceso ingresados no son correctos"
        }), 401
    
@login_manager.user_loader
def load_user(user_id): 
    return User.get_by_id(user_id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()