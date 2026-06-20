# 🛒 Carrinho de Compras Virtual

Projeto desenvolvido para a disciplina de Estruturas de Dados, simulando um sistema de carrinho de compras de uma loja virtual.

---

## 👥 Integrantes

- Matheus Costa Mendes
- João Pedro Borges
- Hideki Wakui Oi

---

## 📌 Tema / Projeto

**Carrinho de Compras Virtual** — sistema que simula o funcionamento de uma loja virtual, com cadastro de produtos, gerenciamento de carrinho, histórico de compras e atualização de estoque em tempo real.

### Funcionalidades implementadas

- Cadastrar produto com nome, preço e quantidade em estoque
- Adicionar e remover produtos do carrinho
- Desfazer a última ação no carrinho (usando **Pilha**)
- Exibir resumo do carrinho com total atualizado
- Finalizar compra — estoque reservado em tempo real ao adicionar ao carrinho
- Exibir histórico de compras realizadas (usando **Lista Encadeada**)
- Ordenar produtos por nome ou preço (usando `sorted()` e `list.sort()` nativos do Python)
- Buscar produto por nome em tempo real

---

## 💻 Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| Frontend | HTML5 + Bootstrap 5 + JavaScript (Fetch API) |
| Backend | Python 3 + Flask |
| Dados | Estruturas em memória: Array, Pilha, Lista Encadeada |

### Estruturas de dados utilizadas

| Estrutura | Onde é usada |
|---|---|
| **Array** (`array.py`) | Catálogo de produtos e itens do carrinho |
| **Pilha** (`pilha.py`) | Histórico de ações para desfazer (undo) |
| **Lista Encadeada** (`lista_encadeada.py`) | Histórico de compras finalizadas |

---

## ▶️ Instruções para Execução

### Pré-requisitos

- Python 3.10 ou superior instalado
- pip (gerenciador de pacotes do Python)

### Passo a passo

**1. Clone o repositório:**
```bash
git clone https://github.com/MatheusW14/Ed-carrinho-de-compras.git
cd Ed-carrinho-de-compras
```

**2. Crie e ative um ambiente virtual:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Execute a aplicação:**
```bash
flask run
```

**5. Acesse no navegador:**
```
http://localhost:5000
```

---

## 📁 Estrutura do Projeto

```
├── app.py                      # Servidor Flask e rotas da API REST
├── requirements.txt            # Dependências do projeto
├── estruturas/
│   ├── __init__.py
│   ├── array.py                # Array dinâmico (catálogo e carrinho)
│   ├── pilha.py                # Pilha para desfazer ações
│   └── lista_encadeada.py      # Lista encadeada para histórico
└── templates/
    └── index.html              # Interface com Bootstrap 5
```

---

## 📄 Licença

Projeto acadêmico — IFMS Campus Três Lagoas. Todos os direitos reservados aos autores.