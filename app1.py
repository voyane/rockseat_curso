# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#Criar a instancia do aplicativo flask
app1 = Flask(__name__) 

#passar a configuracao do caminho de onde fica a base de dados
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
#iniciar a conexao com a bd
db = SQLAlchemy(app1)

#Modelagem
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


#db.create_all().pega todas as modelagens e transforma em tabelas
#session e a propriedade de armazena a conexao. commit salva as mudancas
# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar

@app1.route('/api/products/add', methods = ["POST"])
def add_product():
    data = request.json
#criar produto
    if "name" in data and "price" in data:
        produto = Product(name = data["name"] , price = data["price"], description = data.get("description", ""))
        db.session.add(produto)    
        db.session.commit()
        return jsonify({"mensagem": "Produto cadastrado com sucesso."})
    return jsonify({"message": "Dados do produto invalidos."}), 400

#Apagar o produto
@app1.route('/api/products/delete/<int:produto_id>', methods = ["DELETE"])
def delete_produto(produto_id):
#Recuperar o prpduto da BD
    produto = Product.query.get(produto_id)
#Verificar se o produto existe
    if produto:
#se existir, apaga o produto da BD
        db.session.delete(produto)
        db.session.commit()
        return jsonify({"mensagem": "Produto apagado com sucesso."})
#se nao, retorna o erro 400 not found
    return jsonify({"mensagem": "Erro ao remover o produto."}), 404 

#Recuperar os detalhes do produtp
@app1.route('/api/products/<int:produto_id>', methods = ["GET"])
def get_produto_details(produto_id):
    produto = Product.query.get(produto_id)
    if produto:
        return jsonify({
             "id": produto.id,
             "name": produto.name,
             "price": produto.price,
             "description": produto.description       
        })
    return jsonify({"mensagem": "Produto nao encontrado."}), 404

#Actualizacao
@app1.route("/api/products/update/<int:produto_id>", methods = ["PUT"])
def update_produto(produto_id):
    produto = Product.query.get(produto_id)
    if not produto:
        return jsonify({"mensagem": "Produto nao encontrado."}), 404
    
    data = request.json
    if "name" in data:
        produto.name = data["name"]

    if "price" in data:
        produto.price = data["price"]

    if "description" in data:
        produto.description = data["description"]

    return jsonify({"mensagem": "Produto actualizado com sucesso."})

@app1.route("/")
def hello_world(): #definir a funcao
    return 'Hello World'

if __name__ == "__main__":
    app1.run(debug=True)