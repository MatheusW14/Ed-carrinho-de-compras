class Array:
    def __init__(self):
        self._dados = []

    def inserir(self, elemento):
        self._dados.append(elemento)

    def remover(self, indice):
        if 0 <= indice < len(self._dados):
            return self._dados.pop(indice)

    def listar(self):
        return list(self._dados)

    def tamanho(self):
        return len(self._dados)

    def buscar_por_nome(self, nome):
        resultado = []
        for p in self._dados:
            if nome.lower() in p['nome'].lower():
                resultado.append(p)
        return resultado

    def ordenar_por_nome(self):
        # Bubble Sort pelo nome
        n = len(self._dados)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if self._dados[j]['nome'].lower() > self._dados[j + 1]['nome'].lower():
                    self._dados[j], self._dados[j + 1] = self._dados[j + 1], self._dados[j]

    def ordenar_por_preco(self):
        # Bubble Sort pelo preço
        n = len(self._dados)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if self._dados[j]['preco'] > self._dados[j + 1]['preco']:
                    self._dados[j], self._dados[j + 1] = self._dados[j + 1], self._dados[j]
