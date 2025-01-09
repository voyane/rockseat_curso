# Importação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Criar a instancia do aplicativo flask
app = Flask(__name__) 

#passar a configuracao do caminho de onde fica a base de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
#iniciar a conexao com a bd
db = SQLAlchemy(app)

#Modelagem
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text, nullable = True)


#db.create_all().pega todas as modelagens e transforma em tabelas
#session e a propriedade de armazena a conexao. commit salva as mudancas
# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/') 
def hello_world(): #definir a funcao
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True)