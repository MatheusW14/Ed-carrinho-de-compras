# 🛒 Carrinho de Compras Virtual

Projeto desenvolvido para a disciplina de Estruturas de Dados, simulando um sistema de carrinho de compras de uma loja virtual.

---

## 👥 Integrantes

- Matheus Costa Mendes
- João Pedro Borges
- Hideki Wakui Oi

---

## 📌 Tema / Projeto

**Carrinho de Compras Virtual** — sistema que simula o funcionamento de uma loja virtual, com cadastro de produtos, gerenciamento de carrinho, histórico de compras e atualização de estoque.

### Funcionalidades previstas

- Cadastrar produto com nome, preço e quantidade em estoque
- Adicionar e remover produtos do carrinho
- Desfazer a última ação no carrinho (usando **pilha**)
- Exibir resumo do carrinho com total atualizado
- Finalizar compra e atualizar estoque automaticamente
- Exibir histórico de compras realizadas (usando **lista encadeada**)
- Ordenar produtos por nome ou preço
- Buscar produto por nome ou categoria
- Localização rápida de produto por código (usando **tabela hash**)

---

## 💻 Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|------------|
| Frontend | HTML5 + Bootstrap 5 |
| Backend | Python 3 + Flask |
| Dados | Estruturas em memória (dicionários, listas, pilha, lista encadeada) |

---

## ▶️ Instruções para Execução

### Pré-requisitos

- Python 3.10 ou superior instalado
- pip (gerenciador de pacotes do Python)

### Passo a passo

**1. Clone o repositório:**
```bash
git clone https://github.com/MatheusW14/Ed-carrinho-de-compras.git
cd nome-do-repositorio
```

**2. Crie e ative um ambiente virtual (recomendado):**
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

## 📁 Estrutura do Projeto (prevista)

```
├── app.py                  # Arquivo principal Flask
├── requirements.txt        # Dependências do projeto
├── estruturas/
│   ├── pilha.py            # Implementação da pilha (undo)
│   ├── lista_encadeada.py  # Histórico de compras
│   └── tabela_hash.py      # Busca rápida por código
├── templates/
│   └── index.html          # Interface com Bootstrap
└── static/
    └── style.css           # Estilos adicionais
```

---

## 📄 Licença

Projeto acadêmico — IFMS. Todos os direitos reservados aos autores.
