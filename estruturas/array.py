class Array:
    """
    Classe Array
    Esta classe implementa uma estrutura de dados baseada em lista para armazenar objetos.
    Ela fornece métodos para inserir, remover, listar, buscar e ordenar os elementos armazenados.
    Métodos:
    ---------
    - __init__():
        Inicializa uma nova instância da classe Array.
    - inserir(elemento):
        Adiciona um novo elemento ao final da lista.
    - remover(indice):
        Remove e retorna o elemento no índice especificado, se o índice for válido.
    - listar():
        Retorna uma cópia da lista de elementos armazenados.
    - buscar_por_id(campo, valor):
        Busca um objeto na lista com base no valor de um campo específico e retorna a referência direta ao objeto.
    - tamanho():
        Retorna o número de elementos armazenados na lista.
    - buscar_por_nome(nome):
        Retorna uma lista de objetos cujo campo "nome" contém a string especificada (busca insensível a maiúsculas/minúsculas).
    - ordenar_por_nome():
        Ordena os objetos na lista com base no campo "nome" em ordem alfabética (insensível a maiúsculas/minúsculas).
    - ordenar_por_preco():
        Ordena os objetos na lista com base no campo "preco" em ordem crescente.
    """

    def __init__(self):
        self._dados = []

    def inserir(self, elemento):
        """
        Insere um elemento no final do array.

        Args:
            elemento: O elemento a ser adicionado ao array.
        """
        self._dados.append(elemento)

    def remover(self, indice):
        """
        Remove e retorna o elemento no índice especificado da lista interna.

        Args:
            indice (int): O índice do elemento a ser removido. Deve estar dentro do intervalo válido da lista.

        Returns:
            O elemento removido da lista.

        Raises:
            IndexError: Se o índice estiver fora do intervalo válido da lista.
        """
        if 0 <= indice < len(self._dados):
            return self._dados.pop(indice)

    def listar(self):
        """
        Retorna uma lista contendo todos os elementos armazenados no array.

        Returns:
            list: Uma lista com os elementos do array.
        """
        return list(self._dados)

    def buscar_por_id(self, campo, valor):
        """Retorna a referência direta ao objeto (não uma cópia)."""
        for item in self._dados:
            if item.get(campo) == valor:
                return item
        return None

    def tamanho(self):
        """
        Retorna o tamanho do array.

        Returns:
            int: O número de elementos presentes no array.
        """
        return len(self._dados)

    def buscar_por_nome(self, nome):
        """
        Busca por itens no array cujo nome contenha a string fornecida.

        Args:
            nome (str): A string a ser buscada nos nomes dos itens.

        Returns:
            list: Uma lista de itens (dicionários) cujo nome contém a string fornecida,
            ignorando diferenças entre maiúsculas e minúsculas.
        """
        resultado = []
        for p in self._dados:
            if nome.lower() in p["nome"].lower():
                resultado.append(p)
        return resultado

    def ordenar_por_nome(self):
        """
        Ordena os elementos do array pelo campo "nome" em ordem alfabética,
        desconsiderando diferenças entre maiúsculas e minúsculas.

        Atributos:
            self._dados (list): Lista de dicionários onde cada dicionário deve
            conter a chave "nome" para que a ordenação seja realizada corretamente.
        """
        self._dados.sort(key=lambda p: p["nome"].lower())

    def ordenar_por_preco(self):
        """
        Ordena os itens armazenados em `_dados` com base no preço.

        A ordenação é feita de forma crescente, utilizando o valor associado
        à chave "preco" de cada item no dicionário.

        Returns:
            None: Este método modifica a lista `_dados` diretamente.
        """
        self._dados.sort(key=lambda p: p["preco"])
