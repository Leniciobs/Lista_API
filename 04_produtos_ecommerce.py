from flask import Flask, request, jsonify, make_response
from hashlib import sha256
import json

PRODUTOS_FILE = "produtos.json"
CARRINHO_FILE = "carrinho.json"

app = Flask(__name__)

@app.route('/')
def index():
  return 'Bem-vindo à sua API de Gerenciamento de um E-commerce'

def get_produtos():
    with open(PRODUTOS_FILE, "r") as f:
        produtos = json.load(f)
    f.close()
    return produtos

def save_produtos(produtos):
    with open(PRODUTOS_FILE, "w") as f:
        json.dump(produtos, f, indent=2)

def get_carrinho():
    try:
        with open(CARRINHO_FILE, "r") as f:
            carrinho = json.load(f)
    except FileNotFoundError:
        carrinho = []
    f.close()
    return carrinho

def save_carrinho(carrinho):
    with open(CARRINHO_FILE, "w") as f:
        json.dump(carrinho, f, indent=2)

@app.route("/produtos", methods=["GET"])
def get_produtos():
    produtos = get_produtos()
    return jsonify(produtos)

@app.route("/produtos/<int:id>", methods=["GET"])
def get_produto_por_id(id):
    produtos = get_produtos()
    produto = next((p for p in produtos if p["id"] == id), None)
    if produto is None:
        return make_response({"erro": "Produto não encontrado"}, 404)
    return jsonify(produto)

@app.route("/produtos", methods=["POST"])
def criar_produto():
    data = json.loads(request.data)
    nova_id = max(p["id"] for p in get_produtos()) + 1
    data["id"] = nova_id
    get_produtos().append(data)
    save_produtos(get_produtos())
    return jsonify({"produto": data, "mensagem": "Produto criado com sucesso"})

@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    produtos = get_produtos()
    produto = next((p for p in produtos if p["id"] == id), None)
    if produto is None:
        return make_response({"erro": "Produto não encontrado"}, 404)
    data = json.loads(request.data)
    produto.update(data)
    save_produtos(produtos)
    return jsonify(produto)

@app.route("/produtos/<int:id>/estoque", methods=["PUT"])
def atualizar_estoque(id):
    produtos = get_produtos()
    produto = next((p for p in produtos if p["id"] == id), None)
    if produto is None:
        return make_response({"erro": "Produto não encontrado"}, 404)
    data = json.loads(request.data)
    produto["estoque"] += data["quantidade"]
    if produto["estoque"] < 0:
        return make_response({"erro": "Estoque não pode ser negativo"}, 400)
    save_produtos(produtos)
    return jsonify({"mensagem": "Estoque atualizado com sucesso"})

@app.route("/produtos/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    produtos = get_produtos()
    produto = next((p for p in produtos if p["id"] == id), None)
    if produto is None:
        return make_response({"erro": "Produto não encontrado"}, 404)
    get_produtos().remove(produto)
    save_produtos(produtos)
    return jsonify({"mensagem": "Produto excluído com sucesso"})

@app.route("/carrinho", methods=["GET"])
def get_carrinho():
    carrinho = get_carrinho()
    return jsonify(carrinho)

@app.route("/carrinho", methods=["POST"])
def adicionar_ao_carrinho():
    data = json.loads(request.data)
    produto = next((p for p in get_produtos() if p["id"] == data["produto_id"]), None)
    if produto is None:
        return make_response({"erro": "Produto não encontrado"}, 404)
    if produto["estoque"] < data["quantidade"]:
        return make_response({"erro": "Estoque insuficiente"}, 400)
    carrinho = get_carrinho()
    item_carrinho = next((i for i in carrinho if i["produto_id"] == "produto_id"), None)
    if item_carrinho is None:
        return make_response({"erro": "Item não encontrado no carrinho"}, 404)
    carrinho.remove(item_carrinho)
    save_carrinho(carrinho)
    return jsonify({"mensagem": "Item removido do carrinho com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)
