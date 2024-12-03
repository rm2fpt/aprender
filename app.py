from flask import Flask, render_template
import os

# Criar a instância do Flask
app = Flask(__name__)

# Rota principal
@app.route('/')
def home():
    return render_template('index.html', message='Esta é sua primeira aplicação Flask!')

# Rota adicional que retorna JSON
@app.route('/api/hello')
def hello_api():
    return {'message': 'Olá do Flask!'}

# Rota com parâmetro
@app.route('/saudacao/<nome>')
def saudacao(nome):
    return render_template('index.html', message=f'Olá, {nome}!')

if __name__ == '__main__':
    # Pegar a porta do ambiente (necessário para o deploy)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
