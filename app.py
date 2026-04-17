from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Armazenamento em memória
tarefas = {}

def gerar_id():
    return str(uuid.uuid4())[:8]

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    dados = request.get_json()

    if not dados or not dados.get("titulo") or dados["titulo"].strip() == "":
        return jsonify({"erro": "Título é obrigatório"}), 400

    titulo = dados["titulo"].strip()

    # Verificar título duplicado
    for t in tarefas.values():
        if t["titulo"].lower() == titulo.lower():
            return jsonify({"erro": "Já existe uma tarefa com este título"}), 409

    prioridade = dados.get("prioridade", "Média")
    if prioridade not in ["Alta", "Média", "Baixa"]:
        prioridade = "Média"

    nova_tarefa = {
        "id": gerar_id(),
        "titulo": titulo,
        "descricao": dados.get("descricao", "").strip(),
        "prioridade": prioridade,
        "concluida": False,
        "criada_em": datetime.now().isoformat()
    }

    tarefas[nova_tarefa["id"]] = nova_tarefa
    return jsonify(nova_tarefa), 201

@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    busca = request.args.get("busca", "").strip().lower()

    resultado = list(tarefas.values())

    if busca:
        resultado = [t for t in resultado if busca in t["titulo"].lower()]

    return jsonify(resultado), 200

@app.route("/tarefas/<id>", methods=["GET"])
def buscar_tarefa(id):
    tarefa = tarefas.get(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(tarefa), 200

@app.route("/tarefas/<id>/concluir", methods=["PUT"])
def concluir_tarefa(id):
    tarefa = tarefas.get(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    tarefa["concluida"] = True
    tarefa["concluida_em"] = datetime.now().isoformat()
    return jsonify(tarefa), 200

@app.route("/tarefas/<id>", methods=["DELETE"])
def excluir_tarefa(id):
    tarefa = tarefas.pop(id, None)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify({"mensagem": "Tarefa excluída com sucesso", "tarefa": tarefa}), 200

if __name__ == "__main__":
    print("🚀 Sistema de Tarefas rodando em http://localhost:5000")
    app.run(debug=True, port=5000)