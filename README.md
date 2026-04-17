# TaskFlow – Sistema de Gerenciamento de Tarefas

### AC3 – Quality Assurance | UNIFECAF

---

## 📁 Estrutura de Arquivos

```
todo_app/
├── app.py               ← Back-end Flask (API REST)
├── requirements.txt     ← Dependências Python
├── test_tarefas.py      ← Testes automatizados (pytest)
├── README.md            ← Este arquivo
└── static/
    └── index.html       ← Front-end (HTML/CSS/JS)
```

---

## ⚙️ Instalação e Execução

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o servidor

```bash
python app.py
```

> O sistema estará em: **http://localhost:5000**

### 3. Executar os testes automatizados

> Com o servidor rodando em outra aba do terminal:

```bash
pytest test_tarefas.py -v
```

---

## 🌐 Endpoints da API

| Método | Rota                   | Descrição               |
| ------ | ---------------------- | ----------------------- |
| POST   | /tarefas               | Criar nova tarefa       |
| GET    | /tarefas               | Listar todas as tarefas |
| GET    | /tarefas?busca=xxx     | Buscar por título       |
| PUT    | /tarefas/<id>/concluir | Marcar como concluída   |
| DELETE | /tarefas/<id>          | Excluir tarefa          |

---

## 📦 Exemplos de Payload (Postman / cURL)

### Criar tarefa válida

```json
POST /tarefas
{
  "titulo": "Implementar login",
  "descricao": "Criar tela de autenticação",
  "prioridade": "Alta"
}
```

### Resposta esperada (201)

```json
{
  "id": "a1b2c3d4",
  "titulo": "Implementar login",
  "descricao": "Criar tela de autenticação",
  "prioridade": "Alta",
  "concluida": false,
  "criada_em": "2025-05-01T14:30:00"
}
```

---

## ✅ Casos de Teste (resumo)

| ID    | Descrição                                  | Esperado  |
| ----- | ------------------------------------------ | --------- |
| TC001 | Criar tarefa com dados válidos             | 201       |
| TC002 | Criar tarefa com título vazio              | 400       |
| TC003 | Criar tarefa com título duplicado          | 409       |
| TC004 | Criar tarefa sem prioridade (assume Média) | 201       |
| TC005 | POST sem body                              | 400       |
| TC006 | Listar tarefas quando não há nenhuma       | 200 / []  |
| TC007 | Listar tarefas após criação                | 200 / [2] |
| TC008 | Buscar tarefa por título existente         | 200 / [1] |
| TC009 | Buscar título inexistente                  | 200 / []  |
| TC010 | Concluir tarefa existente                  | 200       |
| TC011 | Concluir tarefa com ID inválido            | 404       |
| TC012 | Excluir tarefa existente                   | 200       |
| TC013 | Excluir tarefa com ID inválido             | 404       |
| TC014 | Título composto só de espaços              | 400       |
| TC015 | Prioridade inválida normalizada para Média | 201       |

---

## 🐛 Bugs Conhecidos (para documentar no AC3)

1. **BUG-01 – Sem persistência:** dados são perdidos ao reiniciar o servidor.
   - _Impacto:_ Médio — todos os dados somem ao parar o processo.
   - _Sugestão:_ Substituir dicionário em memória por SQLite ou arquivo JSON.

2. **BUG-02 – Sem paginação:** a rota GET /tarefas retorna todas as tarefas sem limite.
   - _Impacto:_ Baixo (escala) — com muitas tarefas, a resposta pode ficar lenta.
   - _Sugestão:_ Adicionar parâmetros `page` e `limit`.

---

## 💡 Melhorias Sugeridas

- **Técnica 1:** Adicionar banco de dados SQLite para persistência.
- **Técnica 2:** Implementar autenticação simples (token JWT ou API Key).
- **Geral:** Adicionar feedback visual de loading no front-end durante requisições.
# projeto_qa
