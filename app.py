from flask import Flask, render_template
import os

# Criar a instância do Flask
app = Flask(__name__, 
            template_folder='templates',  # especifica a pasta de templates
            static_folder='static')       # especifica a pasta de arquivos estáticos

# Configuração para produção
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Rota principal
@app.route('/')
def home():
    try:
        return render_template('index.html', message='Esta é sua primeira aplicação Flask!')
    except Exception as e:
        return str(e), 500  # retorna o erro para debug

# Rota adicional que retorna JSON
@app.route('/api/hello')
def hello_api():
    return {'message': 'Olá do Flask!'}

# Rota com parâmetro
@app.route('/saudacao/<nome>')
def saudacao(nome):
    try:
        return render_template('index.html', message=f'Olá, {nome}!')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Pegar a porta do ambiente (necessário para o deploy)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
