# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin , login_user, LoginManager, login_required, logout_user


#Criar a instancia do aplicativo flask
app1 = Flask(__name__) 

app1.config["SECRET_KEY"] = "password7777"
#passar a configuracao do caminho de onde fica a base de dados
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'


login_manager = LoginManager()

#iniciar a conexao com a bd
db = SQLAlchemy(app1)
login_manager.init_app(app1)
login_manager.login_view = "login"
CORS(app1)


#USER (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)
    cart = db.relationship("CarItem", backref = "user", lazy = True)


#Modelagem
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


#db.create_all().pega todas as modelagens e transforma em tabelas
#session e a propriedade de armazena a conexao. commit salva as mudancas
# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar

#Autenticacao
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app1.route('/api/products/add', methods = ["POST"])
#para usar esta rota, precisa estar autenticado.
@login_required
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
@login_required
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
@login_required
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

    db.session.commit()
    return jsonify({"mensagem": "Produto actualizado com sucesso."})


#Listar
@app1.route("/api/products", methods = ["GET"])
def get_produtos():
    produtos = Product.query.all()
    lista_produto = []
    for produto in produtos:
        dados_produto = {
            "id": produto.id,
             "name": produto.name,
             "price": produto.price,
             "description": produto.description
        }
        lista_produto.append(dados_produto)

    return jsonify(lista_produto)


@app1.route("/login", methods = ["POST"])
def login():
    data = request.json
    
    user = User.query.filter_by(username = data.get("username")).first()
    
    if user: 
        if data.get("password") == user.password:
             login_user(user)
             return jsonify({"mensagem": "Acesso Autorizado."})
    return jsonify({"mensagem": "Acesso Nao Autorizado."}), 401

@app1.route("/logout", methods = ["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"mensagem": "Desconectado com sucesso."})


   



@app1.route("/")
def hello_world(): #definir a funcao
    return 'Hello World'

if __name__ == "__main__":
    app1.run(debug=True)
    with app1.app_context():  # Garante o contexto da aplicação
        db.drop_all()  # Apaga todas as tabelas do banco
        db.create_all()  # Cria as tabelas novamente
    app1.run(debug=True)