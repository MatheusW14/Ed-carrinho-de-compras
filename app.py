from datetime import datetime
from flask import Flask, request, jsonify, render_template
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
    """
    Lista os produtos disponíveis, com opções de busca e ordenação.
    Retorna uma lista de produtos no formato JSON. É possível filtrar os produtos
    pelo nome utilizando o parâmetro de busca e ordenar os resultados pelo preço
    ou pelo nome.
    Parâmetros:
        - busca (str, opcional): Termo de busca para filtrar os produtos pelo nome.
        - ordenar (str, opcional): Critério de ordenação dos produtos. Pode ser "preco"
          para ordenar pelo preço ou "nome" para ordenar alfabeticamente pelo nome.
    Retorno:
        - JSON: Lista de produtos, possivelmente filtrada e ordenada conforme os parâmetros.
    """
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
    """
    Cadastra um novo produto no sistema.
    Este endpoint recebe os dados de um produto via JSON no corpo da requisição,
    valida as informações fornecidas e, se estiverem corretas, insere o produto
    na base de dados.
    Retorna:
        - 201 Created: Se o produto for cadastrado com sucesso, retorna os dados do produto.
        - 400 Bad Request: Se houver algum erro de validação nos dados fornecidos.
    Campos esperados no corpo da requisição:
        - nome (str): Nome do produto (obrigatório, não pode ser vazio).
        - preco (float): Preço do produto (obrigatório, deve ser maior ou igual a 0).
        - quantidade (int): Quantidade do produto (obrigatório, deve ser maior ou igual a 0).
    Exemplo de corpo da requisição:
    {
        "nome": "Produto Exemplo",
        "preco": 19.99,
        "quantidade": 10
    Exemplo de resposta de sucesso:
    {
        "id": 1,
        "nome": "Produto Exemplo",
        "preco": 19.99,
        "quantidade": 10
    """
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
    """
    Remove um produto da lista de produtos com base no ID fornecido.

    Args:
        produto_id (int): O ID do produto a ser removido.

    Returns:
        Response: Um objeto JSON com uma mensagem de sucesso se o produto for removido,
        ou uma mensagem de erro e código de status 404 se o produto não for encontrado.
    """
    lista = produtos.listar()
    for i, p in enumerate(lista):
        if p["id"] == produto_id:
            produtos.remover(i)
            return jsonify({"mensagem": "Produto removido"})
    return jsonify({"erro": "Produto não encontrado"}), 404


# ─── CARRINHO ────────────────────────────────────────────


@app.route("/carrinho", methods=["GET"])
def ver_carrinho():
    """
    Retorna os itens do carrinho e o valor total da compra.

    Esta função obtém a lista de itens presentes no carrinho, calcula o valor
    total com base no preço e na quantidade de cada item, e retorna os dados
    em formato JSON.

    Retorna:
        dict: Um dicionário contendo:
            - "itens" (list): Lista de itens no carrinho, onde cada item é um
              dicionário com informações como "preco" e "quantidade_carrinho".
            - "total" (float): O valor total da compra, arredondado para duas
              casas decimais.
    """
    itens = carrinho.listar()
    total = sum(i["preco"] * i["quantidade_carrinho"] for i in itens)
    return jsonify({"itens": itens, "total": round(total, 2)})


@app.route("/carrinho", methods=["POST"])
def adicionar_ao_carrinho():
    """
    Adiciona um produto ao carrinho de compras.
    Esta função recebe os dados de um produto via corpo da requisição JSON,
    valida as informações fornecidas e adiciona o produto ao carrinho de compras.
    Caso o produto já esteja no carrinho, a quantidade será atualizada.
    O estoque do produto é reservado imediatamente ao adicioná-lo ao carrinho.
    Retornos:
        - 400: Se o corpo da requisição for inválido, se o produto_id não for fornecido,
          se a quantidade for menor ou igual a zero, ou se o estoque for insuficiente.
        - 404: Se o produto não for encontrado.
        - 200: Se o produto já estiver no carrinho e a quantidade for atualizada.
        - 201: Se o produto for adicionado ao carrinho com sucesso.
    Estrutura do corpo da requisição (JSON):
        {
            "produto_id": <str>,  # ID do produto (obrigatório)
            "quantidade": <int>   # Quantidade do produto (opcional, padrão: 1)
    Estrutura do retorno (JSON):
        - Em caso de sucesso:
            {
                "produto_id": <str>,       # ID do produto
                "nome": <str>,             # Nome do produto
                "preco": <float>,          # Preço do produto
                "quantidade_carrinho": <int>  # Quantidade adicionada ao carrinho
        - Em caso de erro:
            {
                "erro": <str>  # Mensagem de erro
    """
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
    """
    Remove um item do carrinho de compras com base no ID do produto.

    Ao remover o item do carrinho:
    - A quantidade do produto é devolvida ao estoque.
    - A ação de remoção é registrada na pilha de "undo" para permitir desfazer a operação.

    Args:
        produto_id (int): O ID do produto a ser removido do carrinho.

    Returns:
        Response: Um objeto JSON com uma mensagem de sucesso se o item for removido,
                  ou uma mensagem de erro com código 404 se o item não for encontrado.
    """
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
    """
    Desfaz a última ação realizada no carrinho de compras.
    Esta função utiliza uma pilha de ações (pilha_undo) para reverter a última
    operação realizada no carrinho de compras. As ações suportadas são:
    - "adicionar": Remove o item adicionado ao carrinho e devolve a quantidade ao estoque.
    - "remover": Reinsere o item removido ao carrinho e ajusta o estoque.
    Retorna:
        flask.Response: Um objeto JSON contendo uma mensagem indicando o resultado da operação.
        - {"mensagem": "Nada para desfazer"}: Caso não haja ações para desfazer.
        - {"mensagem": "Adição desfeita"}: Caso uma adição tenha sido desfeita.
        - {"mensagem": "Remoção desfeita"}: Caso uma remoção tenha sido desfeita.
    """
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
    """
    Finaliza a compra do carrinho de compras.
    Esta função verifica se o carrinho contém itens. Caso esteja vazio, retorna um erro.
    Caso contrário, calcula o total da compra, registra o histórico da compra e limpa o carrinho.
    Também esvazia a pilha de ações de desfazer (undo).
    Retorna:
        dict: Um dicionário contendo uma mensagem de sucesso e os detalhes da compra realizada.
        tuple: Em caso de erro, retorna um dicionário com a mensagem de erro e o código HTTP 400.
    """
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
    """
    Retorna o histórico de compras em formato JSON.

    Esta função utiliza o método `listar` do objeto `historico` para obter
    os dados do histórico de compras e os retorna como uma resposta JSON.

    Returns:
        Response: Um objeto JSON contendo o histórico de compras.
    """
    return jsonify(historico.listar())


if __name__ == "__main__":
    app.run(debug=True)
