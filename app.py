# Importação
from flask import Flask

#Criar a instancia do aplicativo flask
app = Flask(__name__) 

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/') 
def hello_world(): #definir a funcao
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True)