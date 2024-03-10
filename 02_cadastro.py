from flask import Flask, request, jsonify, make_response
from hashlib import sha256
import json

app = Flask(__name__)

USUARIOS_FILE = "usuarios.json"

@app.route('/')
def index():
  return 'Bem-vindo à sua API Cadastro Clientes'

def get_usuarios():
    with open(USUARIOS_FILE, "r") as f:
        usuarios = json.load(f)
    f.close()
    return usuarios

def save_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=2)

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = get_usuarios()
    return jsonify(usuarios)

@app.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario_por_id(id):
    usuarios = get_usuarios()
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario is None:
        return make_response({"erro": "Usuário não encontrado"}, 404)
    return jsonify(usuario)

@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    data = json.loads(request.data)
    data["senha"] = sha256(data["senha"].encode()).hexdigest()

    usuarios = get_usuarios()
    novo_id = max(u["id"] for u in usuarios) + 1
    data["id"] = novo_id
    usuarios.append(data)

    save_usuarios(usuarios)

    return jsonify({"usuario": data, "mensagem": "Usuário criado com sucesso"})

@app.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    usuarios = get_usuarios()
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario is None:
        return make_response({"erro": "Usuário não encontrado"}, 404)

    data = json.loads(request.data)
    usuario.update(data)

    save_usuarios(usuarios)

    return jsonify(usuario)

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    usuarios = get_usuarios()
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario is None:
        return make_response({"erro": "Usuário não encontrado"}, 404)

    usuarios.remove(usuario)
    save_usuarios(usuarios)

    return jsonify({"mensagem": "Usuário excluído com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)
