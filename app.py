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


# ─── PÁGINA PRINCIPAL ────────────────────────────────────


@app.route("/")
def index():
    return render_template("index.html")


# ─── PRODUTOS ────────────────────────────────────────────


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    busca = request.args.get("busca", "").strip()
    ordenar = request.args.get("ordenar", "").strip()

    if busca:
        resultado = produtos.buscar_por_nome(busca)
    else:
        resultado = produtos.listar()

    if ordenar == "preco":
        resultado = sorted(resultado, key=lambda p: p["preco"])
    elif ordenar == "nome":
        resultado = sorted(resultado, key=lambda p: p["nome"].lower())

    return jsonify(resultado)


@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    nome = str(dados.get("nome", "")).strip()
    preco = dados.get("preco")
    quantidade = dados.get("quantidade")

    if not nome:
        return jsonify({"erro": "Nome do produto é obrigatório"}), 400
    if preco is None or float(preco) < 0:
        return jsonify({"erro": "Preço inválido"}), 400
    if quantidade is None or int(quantidade) < 0:
        return jsonify({"erro": "Quantidade inválida"}), 400

    produto = {
        "id": proximo_id["value"],
        "nome": nome,
        "preco": round(float(preco), 2),
        "quantidade": int(quantidade),
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


# ─── CARRINHO ────────────────────────────────────────────


@app.route("/carrinho", methods=["GET"])
def ver_carrinho():
    itens = carrinho.listar()
    total = sum(i["preco"] * i["quantidade_carrinho"] for i in itens)
    return jsonify({"itens": itens, "total": round(total, 2)})


@app.route("/carrinho", methods=["POST"])
def adicionar_ao_carrinho():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade", 1)

    if not produto_id:
        return jsonify({"erro": "produto_id é obrigatório"}), 400
    if int(quantidade) <= 0:
        return jsonify({"erro": "Quantidade deve ser maior que zero"}), 400

    quantidade = int(quantidade)
    produto = produtos.buscar_por_id("id", produto_id)

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    if produto["quantidade"] < quantidade:
        return (
            jsonify(
                {"erro": f"Estoque insuficiente. Disponível: {produto['quantidade']}"}
            ),
            400,
        )

    # Reserva o estoque imediatamente ao adicionar no carrinho
    produto["quantidade"] -= quantidade

    item_carrinho = carrinho.buscar_por_id("produto_id", produto_id)
    if item_carrinho:
        item_carrinho["quantidade_carrinho"] += quantidade
        pilha_undo.empilhar(
            {"acao": "adicionar", "produto_id": produto_id, "quantidade": quantidade}
        )
        return jsonify(item_carrinho), 200

    item = {
        "produto_id": produto_id,
        "nome": produto["nome"],
        "preco": produto["preco"],
        "quantidade_carrinho": quantidade,
    }
    carrinho.inserir(item)
    pilha_undo.empilhar(
        {"acao": "adicionar", "produto_id": produto_id, "quantidade": quantidade}
    )
    return jsonify(item), 201


@app.route("/carrinho/<int:produto_id>", methods=["DELETE"])
def remover_do_carrinho(produto_id):
    itens = carrinho.listar()
    for i, item in enumerate(itens):
        if item["produto_id"] == produto_id:
            removido = carrinho.remover(i)
            # Devolve a quantidade ao estoque ao remover do carrinho
            produto = produtos.buscar_por_id("id", produto_id)
            if produto:
                produto["quantidade"] += removido["quantidade_carrinho"]
            pilha_undo.empilhar({"acao": "remover", "item": removido})
            return jsonify({"mensagem": "Item removido do carrinho"})
    return jsonify({"erro": "Item não encontrado no carrinho"}), 404


@app.route("/carrinho/desfazer", methods=["POST"])
def desfazer():
    acao = pilha_undo.desempilhar()
    if not acao:
        return jsonify({"mensagem": "Nada para desfazer"})

    if acao["acao"] == "adicionar":
        # Desfaz adição: remove do carrinho e devolve ao estoque
        item_carrinho = carrinho.buscar_por_id("produto_id", acao["produto_id"])
        if item_carrinho:
            item_carrinho["quantidade_carrinho"] -= acao["quantidade"]
            produto = produtos.buscar_por_id("id", acao["produto_id"])
            if produto:
                produto["quantidade"] += acao["quantidade"]
            if item_carrinho["quantidade_carrinho"] <= 0:
                idx = carrinho.listar().index(item_carrinho)
                carrinho.remover(idx)
        return jsonify({"mensagem": "Adição desfeita"})

    if acao["acao"] == "remover":
        # Desfaz remoção: volta o item pro carrinho e reserva o estoque novamente
        item = acao["item"]
        produto = produtos.buscar_por_id("id", item["produto_id"])
        if produto:
            produto["quantidade"] -= item["quantidade_carrinho"]
        carrinho.inserir(item)
        return jsonify({"mensagem": "Remoção desfeita"})


# ─── COMPRA ──────────────────────────────────────────────


@app.route("/compra/finalizar", methods=["POST"])
def finalizar_compra():
    itens = carrinho.listar()
    if not itens:
        return jsonify({"erro": "Carrinho vazio"}), 400

    total = sum(i["preco"] * i["quantidade_carrinho"] for i in itens)

    # Estoque já foi decrementado ao adicionar no carrinho,
    # então só precisa limpar o carrinho e registrar o histórico
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


# ─── HISTÓRICO ───────────────────────────────────────────


@app.route("/historico", methods=["GET"])
def ver_historico():
    return jsonify(historico.listar())


if __name__ == "__main__":
    app.run(debug=True)
