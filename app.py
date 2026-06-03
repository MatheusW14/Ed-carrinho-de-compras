from flask import Flask, request, jsonify, render_template
from datetime import datetime
from estruturas.array import Array
from estruturas.pilha import Pilha
from estruturas.lista_encadeada import ListaEncadeada

app = Flask(__name__)

produtos = Array()
carrinho = Array()
pilha_undo = Pilha()
historico = ListaEncadeada()

proximo_id = {"value": 1}


@app.route("/")
def index():
    return render_template("index.html")


# ─── PRODUTOS ────────────────────────────────────────────

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos.listar())


@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()
    produto = {
        "id": proximo_id["value"],
        "nome": dados["nome"],
        "preco": float(dados["preco"]),
        "quantidade": int(dados["quantidade"]),
    }
    produtos.inserir(produto)
    proximo_id["value"] += 1
    return jsonify(produto), 201


@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def remover_produto(produto_id):
    lista = produtos.listar()
    for i, p in enumerate(lista):
        if p["id"] == produto_id:
            produtos.remover(i)
            return jsonify({"mensagem": "Produto removido"})
    return jsonify({"erro": "Produto não encontrado"}), 404


@app.route("/produtos/buscar", methods=["GET"])
def buscar_produto():
    nome = request.args.get("nome", "")
    return jsonify(produtos.buscar_por_nome(nome))


@app.route("/produtos/ordenar", methods=["GET"])
def ordenar_produtos():
    criterio = request.args.get("por", "nome")
    if criterio == "preco":
        produtos.ordenar_por_preco()
    else:
        produtos.ordenar_por_nome()
    return jsonify(produtos.listar())


# ─── CARRINHO ────────────────────────────────────────────

@app.route("/carrinho", methods=["GET"])
def ver_carrinho():
    itens = carrinho.listar()
    total = sum(i["preco"] * i["quantidade_carrinho"] for i in itens)
    return jsonify({"itens": itens, "total": round(total, 2)})


@app.route("/carrinho/adicionar", methods=["POST"])
def adicionar_ao_carrinho():
    dados = request.get_json()
    produto_id = dados["produto_id"]
    quantidade = int(dados["quantidade"])

    produto = None
    for p in produtos.listar():
        if p["id"] == produto_id:
            produto = p
            break

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    if produto["quantidade"] < quantidade:
        return jsonify({"erro": "Quantidade insuficiente em estoque"}), 400

    itens = carrinho.listar()
    for item in itens:
        if item["produto_id"] == produto_id:
            item["quantidade_carrinho"] += quantidade
            pilha_undo.empilhar({"acao": "adicionar", "produto_id": produto_id, "quantidade": quantidade})
            return jsonify(item), 200

    item = {
        "produto_id": produto_id,
        "nome": produto["nome"],
        "preco": produto["preco"],
        "quantidade_carrinho": quantidade,
    }
    carrinho.inserir(item)
    pilha_undo.empilhar({"acao": "adicionar", "produto_id": produto_id, "quantidade": quantidade})
    return jsonify(item), 201


@app.route("/carrinho/remover/<int:produto_id>", methods=["DELETE"])
def remover_do_carrinho(produto_id):
    itens = carrinho.listar()
    for i, item in enumerate(itens):
        if item["produto_id"] == produto_id:
            removido = carrinho.remover(i)
            pilha_undo.empilhar({"acao": "remover", "item": removido})
            return jsonify({"mensagem": "Item removido do carrinho"})
    return jsonify({"erro": "Item não encontrado no carrinho"}), 404


@app.route("/carrinho/desfazer", methods=["POST"])
def desfazer():
    acao = pilha_undo.desempilhar()
    if not acao:
        return jsonify({"mensagem": "Nada para desfazer"})

    if acao["acao"] == "adicionar":
        itens = carrinho.listar()
        for i, item in enumerate(itens):
            if item["produto_id"] == acao["produto_id"]:
                item["quantidade_carrinho"] -= acao["quantidade"]
                if item["quantidade_carrinho"] <= 0:
                    carrinho.remover(i)
                break
        return jsonify({"mensagem": "Adição desfeita"})

    if acao["acao"] == "remover":
        carrinho.inserir(acao["item"])
        return jsonify({"mensagem": "Remoção desfeita"})


# ─── COMPRA ──────────────────────────────────────────────

@app.route("/compra/finalizar", methods=["POST"])
def finalizar_compra():
    itens = carrinho.listar()
    if not itens:
        return jsonify({"erro": "Carrinho vazio"}), 400

    total = sum(i["preco"] * i["quantidade_carrinho"] for i in itens)

    todos_produtos = produtos.listar()
    for item in itens:
        for p in todos_produtos:
            if p["id"] == item["produto_id"]:
                p["quantidade"] -= item["quantidade_carrinho"]

    compra = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "itens": list(itens),
        "total": round(total, 2),
    }
    historico.inserir(compra)

    for _ in range(carrinho.tamanho()):
        carrinho.remover(0)
    while not pilha_undo.esta_vazia():
        pilha_undo.desempilhar()

    return jsonify({"mensagem": "Compra finalizada!", "compra": compra})


@app.route("/historico", methods=["GET"])
def ver_historico():
    return jsonify(historico.listar())


if __name__ == "__main__":
    app.run(debug=True)