from flask import Flask, request, jsonify
from datetime import datetime
from estruturas.array import Array
from estruturas.pilha import Pilha
from estruturas.lista_encadeada import ListaEncadeada
from estruturas.tabela_hash import TabelaHash

app = Flask(__name__)

# Estruturas de dados
produtos = Array()
carrinho = Array()
historico = ListaEncadeada()
pilha_undo = Pilha()
hash_produtos = TabelaHash()

proximo_id = 1


# ─── PRODUTOS ────────────────────────────────────────────

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos.listar())


@app.route('/produtos', methods=['POST'])
def cadastrar_produto():
    global proximo_id
    dados = request.get_json()

    produto = {
        'id': proximo_id,
        'nome': dados['nome'],
        'preco': float(dados['preco']),
        'quantidade': int(dados['quantidade'])
    }

    produtos.inserir(produto)
    hash_produtos.inserir(proximo_id, produto)
    proximo_id += 1

    return jsonify(produto), 201


@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def remover_produto(produto_id):
    lista = produtos.listar()
    for i, p in enumerate(lista):
        if p['id'] == produto_id:
            produtos.remover(i)
            hash_produtos.remover(produto_id)
            return jsonify({'mensagem': 'Produto removido'})
    return jsonify({'erro': 'Produto não encontrado'}), 404


@app.route('/produtos/buscar', methods=['GET'])
def buscar_produto():
    nome = request.args.get('nome', '')
    resultado = produtos.buscar_por_nome(nome)
    return jsonify(resultado)


@app.route('/produtos/ordenar', methods=['GET'])
def ordenar_produtos():
    criterio = request.args.get('por', 'nome')
    if criterio == 'preco':
        produtos.ordenar_por_preco()
    else:
        produtos.ordenar_por_nome()
    return jsonify(produtos.listar())


@app.route('/produtos/codigo/<int:codigo>', methods=['GET'])
def buscar_por_codigo(codigo):
    produto = hash_produtos.buscar(codigo)
    if produto:
        return jsonify(produto)
    return jsonify({'erro': 'Produto não encontrado'}), 404


# ─── CARRINHO ────────────────────────────────────────────

@app.route('/carrinho', methods=['GET'])
def ver_carrinho():
    itens = carrinho.listar()
    total = sum(i['preco'] * i['quantidade_carrinho'] for i in itens)
    return jsonify({'itens': itens, 'total': round(total, 2)})


@app.route('/carrinho/adicionar', methods=['POST'])
def adicionar_ao_carrinho():
    dados = request.get_json()
    produto_id = dados['produto_id']
    quantidade = int(dados['quantidade'])

    produto = hash_produtos.buscar(produto_id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    if produto['quantidade'] < quantidade:
        return jsonify({'erro': 'Quantidade insuficiente em estoque'}), 400

    item = {
        'produto_id': produto_id,
        'nome': produto['nome'],
        'preco': produto['preco'],
        'quantidade_carrinho': quantidade
    }

    carrinho.inserir(item)
    pilha_undo.empilhar({'acao': 'adicionar', 'indice': carrinho.tamanho() - 1})

    return jsonify(item), 201


@app.route('/carrinho/remover/<int:produto_id>', methods=['DELETE'])
def remover_do_carrinho(produto_id):
    itens = carrinho.listar()
    for i, item in enumerate(itens):
        if item['produto_id'] == produto_id:
            removido = carrinho.remover(i)
            pilha_undo.empilhar({'acao': 'remover', 'item': removido})
            return jsonify({'mensagem': 'Item removido do carrinho'})
    return jsonify({'erro': 'Item não encontrado no carrinho'}), 404


@app.route('/carrinho/desfazer', methods=['POST'])
def desfazer():
    acao = pilha_undo.desempilhar()
    if not acao:
        return jsonify({'mensagem': 'Nada para desfazer'})

    if acao['acao'] == 'adicionar':
        carrinho.remover(acao['indice'])
        return jsonify({'mensagem': 'Adição desfeita'})

    if acao['acao'] == 'remover':
        carrinho.inserir(acao['item'])
        return jsonify({'mensagem': 'Remoção desfeita'})


# ─── COMPRA ──────────────────────────────────────────────

@app.route('/compra/finalizar', methods=['POST'])
def finalizar_compra():
    itens = carrinho.listar()
    if not itens:
        return jsonify({'erro': 'Carrinho vazio'}), 400

    total = sum(i['preco'] * i['quantidade_carrinho'] for i in itens)

    # Atualiza estoque
    todos_produtos = produtos.listar()
    for item in itens:
        for p in todos_produtos:
            if p['id'] == item['produto_id']:
                p['quantidade'] -= item['quantidade_carrinho']
                hash_produtos.inserir(p['id'], p)

    compra = {
        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'itens': itens,
        'total': round(total, 2)
    }
    historico.inserir(compra)

    # Limpa o carrinho e a pilha
    for _ in range(carrinho.tamanho()):
        carrinho.remover(0)
    while not pilha_undo.esta_vazia():
        pilha_undo.desempilhar()

    return jsonify({'mensagem': 'Compra finalizada!', 'compra': compra})


@app.route('/historico', methods=['GET'])
def ver_historico():
    return jsonify(historico.listar())


if __name__ == '__main__':
    app.run(debug=True)
