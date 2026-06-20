class No:
    """
    Classe que representa um nó em uma lista encadeada.

    Atributos:
        dado: O valor armazenado no nó.
        proximo: Referência para o próximo nó na lista encadeada (inicialmente None).
    """

    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    """
    Classe que implementa uma lista encadeada simples.
    Métodos:
        __init__:
            Inicializa uma nova lista encadeada vazia.
        inserir(dado):
            Insere um novo nó no início da lista com o dado fornecido.
        listar():
            Retorna uma lista contendo todos os elementos armazenados na lista encadeada.
        esta_vazia():
            Verifica se a lista encadeada está vazia.
    Atributos:
        _cabeca:
            Referência para o primeiro nó da lista encadeada. Inicialmente é None.
    """

    def __init__(self):
        self._cabeca = None

    def inserir(self, dado):
        """
        Insere um novo nó no início da lista encadeada.

        Args:
            dado: O valor a ser armazenado no novo nó.
        """
        novo = No(dado)
        novo.proximo = self._cabeca
        self._cabeca = novo

    def listar(self):
        """
        Retorna uma lista contendo todos os elementos armazenados na lista encadeada.

        Percorre a lista encadeada a partir da cabeça, coletando os dados de cada nó
        e os adicionando a uma lista Python. O processo continua até que não haja mais
        nós na lista.

        Returns:
            list: Uma lista contendo os dados de todos os nós da lista encadeada.
        """
        resultado = []
        atual = self._cabeca
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def esta_vazia(self):
        """
        Verifica se a lista encadeada está vazia.

        Retorna:
            bool: True se a lista estiver vazia (cabeça for None), caso contrário, False.
        """
        return self._cabeca is None
