from flask import Flask, request, jsonify, make_response
import json

TAREFAS_FILE = "tarefas.json"

app = Flask(__name__)

@app.route('/')
def index():
  return 'Bem-vindo à sua API Lista de Tarefas'

def get_tarefas():
    with open(TAREFAS_FILE, "r") as f:
        tarefas = json.load(f)
    f.close()
    return tarefas

def save_tarefas(tarefas):
    with open(TAREFAS_FILE, "w") as f:
        json.dump(tarefas, f, indent=2)

@app.route("/tarefas", methods=["GET"])
def get_tarefas():
    tarefas = get_tarefas()
    return jsonify(tarefas)

@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    data = json.loads(request.data)
    nova_id = max(t["id"] for t in get_tarefas()) + 1
    data["id"] = nova_id
    data["concluida"] = False
    get_tarefas().append(data)
    save_tarefas(get_tarefas())
    return jsonify({"tarefa": data, "mensagem": "Tarefa criada com sucesso"})

@app.route("/tarefas/<int:id>", methods=["GET"])
def get_tarefa_por_id(id):
    tarefas = get_tarefas()
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa is None:
        return make_response({"erro": "Tarefa não encontrada"}, 404)
    return jsonify(tarefa)

@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    tarefas = get_tarefas()
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa is None:
        return make_response({"erro": "Tarefa não encontrada"}, 404)
    data = json.loads(request.data)
    tarefa.update(data)
    save_tarefas(tarefas)
    return jsonify(tarefa)

@app.route("/tarefas/<int:id>/concluir", methods=["PUT"])
def concluir_tarefa(id):
    tarefas = get_tarefas()
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa is None:
        return make_response({"erro": "Tarefa não encontrada"}, 404)
    tarefa["concluida"] = True
    save_tarefas(tarefas)
    return jsonify({"mensagem": "Tarefa concluída com sucesso"})

@app.route("/tarefas/<int:id>", methods=["DELETE"])
def excluir_tarefa(id):
    tarefas = get_tarefas()
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa is None:
        return make_response({"erro": "Tarefa não encontrada"}, 404)
    get_tarefas().remove(tarefa)
    save_tarefas(get_tarefas())
    return jsonify({"mensagem": "Tarefa excluída com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)
