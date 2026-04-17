"""
test_tarefas.py – Testes automatizados para o Sistema de Gerenciamento de Tarefas
Disciplina: Quality Assurance – AC3
Execução: pytest test_tarefas.py -v
"""

import requests
import pytest

BASE_URL = "http://localhost:5000"


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture(autouse=True)
def limpar_estado():
    """
    Como o armazenamento é em memória, esta fixture garante isolamento
    excluindo todas as tarefas antes de cada teste.
    """
    tarefas = requests.get(f"{BASE_URL}/tarefas").json()
    for t in tarefas:
        requests.delete(f"{BASE_URL}/tarefas/{t['id']}")
    yield


# ─────────────────────────────────────────────
# BLOCO 1 – Criação de tarefas (POST /tarefas)
# ─────────────────────────────────────────────

def test_TC001_criar_tarefa_valida():
    """TC001 – Criar tarefa com dados válidos deve retornar 201."""
    payload = {"titulo": "Implementar login", "descricao": "Tela de autenticação", "prioridade": "Alta"}
    res = requests.post(f"{BASE_URL}/tarefas", json=payload)
    assert res.status_code == 201, f"Esperado 201, recebido {res.status_code}"
    data = res.json()
    assert data["titulo"] == "Implementar login"
    assert data["prioridade"] == "Alta"
    assert data["concluida"] == False
    assert "id" in data


def test_TC002_criar_tarefa_sem_titulo():
    """TC002 – Título vazio deve retornar 400."""
    payload = {"titulo": "", "descricao": "Sem título"}
    res = requests.post(f"{BASE_URL}/tarefas", json=payload)
    assert res.status_code == 400, f"Esperado 400, recebido {res.status_code}"
    assert "erro" in res.json()


def test_TC003_criar_tarefa_titulo_duplicado():
    """TC003 – Título duplicado deve retornar 409."""
    payload = {"titulo": "Tarefa Duplicada"}
    requests.post(f"{BASE_URL}/tarefas", json=payload)
    res = requests.post(f"{BASE_URL}/tarefas", json=payload)
    assert res.status_code == 409, f"Esperado 409, recebido {res.status_code}"
    assert "erro" in res.json()


def test_TC004_criar_tarefa_prioridade_padrao():
    """TC004 – Sem prioridade, deve assumir 'Média'."""
    payload = {"titulo": "Tarefa Sem Prioridade"}
    res = requests.post(f"{BASE_URL}/tarefas", json=payload)
    assert res.status_code == 201
    assert res.json()["prioridade"] == "Média"


def test_TC005_criar_tarefa_sem_body():
    """TC005 – Requisição sem body deve retornar 400."""
    res = requests.post(f"{BASE_URL}/tarefas", json={})
    assert res.status_code == 400


# ─────────────────────────────────────────────
# BLOCO 2 – Listagem (GET /tarefas)
# ─────────────────────────────────────────────

def test_TC006_listar_tarefas_vazia():
    """TC006 – Lista vazia deve retornar array vazio com 200."""
    res = requests.get(f"{BASE_URL}/tarefas")
    assert res.status_code == 200
    assert res.json() == []


def test_TC007_listar_tarefas_com_dados():
    """TC007 – Após criar tarefas, listagem deve retorná-las."""
    requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Tarefa A"})
    requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Tarefa B"})
    res = requests.get(f"{BASE_URL}/tarefas")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_TC008_buscar_por_titulo():
    """TC008 – Busca por substring do título deve filtrar resultados."""
    requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Teste de API"})
    requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Deploy na nuvem"})
    res = requests.get(f"{BASE_URL}/tarefas?busca=API")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert "API" in data[0]["titulo"]


def test_TC009_buscar_titulo_inexistente():
    """TC009 – Busca sem match deve retornar lista vazia."""
    requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Tarefa Qualquer"})
    res = requests.get(f"{BASE_URL}/tarefas?busca=xyzabc123")
    assert res.status_code == 200
    assert res.json() == []


# ─────────────────────────────────────────────
# BLOCO 3 – Concluir tarefa (PUT /tarefas/<id>/concluir)
# ─────────────────────────────────────────────

def test_TC010_concluir_tarefa_valida():
    """TC010 – Concluir tarefa existente deve retornar 200 e concluida=True."""
    criacao = requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Tarefa para concluir"})
    tarefa_id = criacao.json()["id"]
    res = requests.put(f"{BASE_URL}/tarefas/{tarefa_id}/concluir")
    assert res.status_code == 200
    assert res.json()["concluida"] == True


def test_TC011_concluir_tarefa_id_invalido():
    """TC011 – Concluir tarefa com ID inexistente deve retornar 404."""
    res = requests.put(f"{BASE_URL}/tarefas/id-inexistente/concluir")
    assert res.status_code == 404
    assert "erro" in res.json()


# ─────────────────────────────────────────────
# BLOCO 4 – Excluir tarefa (DELETE /tarefas/<id>)
# ─────────────────────────────────────────────

def test_TC012_excluir_tarefa_valida():
    """TC012 – Excluir tarefa existente deve retornar 200."""
    criacao = requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Tarefa para deletar"})
    tarefa_id = criacao.json()["id"]
    res = requests.delete(f"{BASE_URL}/tarefas/{tarefa_id}")
    assert res.status_code == 200
    # Confirmar que sumiu da lista
    lista = requests.get(f"{BASE_URL}/tarefas").json()
    ids = [t["id"] for t in lista]
    assert tarefa_id not in ids


def test_TC013_excluir_tarefa_id_invalido():
    """TC013 – Excluir tarefa com ID inexistente deve retornar 404."""
    res = requests.delete(f"{BASE_URL}/tarefas/nao-existe-999")
    assert res.status_code == 404
    assert "erro" in res.json()


# ─────────────────────────────────────────────
# BLOCO 5 – Testes de erro proposital
# ─────────────────────────────────────────────

def test_TC014_titulo_somente_espacos():
    """TC014 – Título composto só de espaços deve ser rejeitado (400)."""
    res = requests.post(f"{BASE_URL}/tarefas", json={"titulo": "   "})
    assert res.status_code == 400


def test_TC015_prioridade_invalida_assume_media():
    """TC015 – Prioridade inválida deve ser normalizada para 'Média'."""
    res = requests.post(f"{BASE_URL}/tarefas", json={"titulo": "Prioridade Estranha", "prioridade": "Urgente"})
    assert res.status_code == 201
    assert res.json()["prioridade"] == "Média"