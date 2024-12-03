from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from dotenv import load_dotenv
import json
import requests
from auth import User

# Carregar variáveis de ambiente
load_dotenv()

# Criar a instância do Flask
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Configuração do Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-padrao')
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Rota principal
@app.route('/')
def home():
    return render_template('index.html', 
                         message='Esta é sua primeira aplicação Flask!',
                         google_client_id=os.getenv('GOOGLE_CLIENT_ID'))

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            user = response.user
            if user:
                login_user(User(user))
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Erro no login. Por favor, verifique suas credenciais.', 'danger')
    
    return render_template('login.html', google_client_id=os.getenv('GOOGLE_CLIENT_ID'))

# Rota do Dashboard (protegida)
@app.route('/dashboard')
@login_required
def dashboard():
    return "Bem-vindo ao Dashboard!"

# Rota para login com Google
@app.route('/google-login', methods=['POST'])
def google_login():
    try:
        token = request.json.get('credential')
        if not token:
            return jsonify({"success": False, "error": "No token provided"}), 400

        # Verificar o token com a API do Google
        google_response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': token}
        )
        
        if google_response.status_code != 200:
            return jsonify({"success": False, "error": "Invalid token"}), 400
            
        user_info = google_response.json()
        
        # Verificar se o email foi verificado pelo Google
        if not user_info.get('email_verified'):
            return jsonify({"success": False, "error": "Email not verified"}), 400

        # Criar ou atualizar usuário no Supabase
        try:
            response = supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "id_token": token
            })
            
            if response.user:
                login_user(User(response.user))
                return jsonify({"success": True, "redirect": url_for('dashboard')})
            
        except Exception as e:
            print(f"Erro Supabase: {str(e)}")
            return jsonify({"success": False, "error": "Authentication failed"}), 400

    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

# Rota de registro
@app.route('/register')
def register():
    return "Página de registro em construção"

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
