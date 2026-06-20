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

    def buscar_por_id(self, campo, valor):
        """Retorna a referência direta ao objeto (não uma cópia)."""
        for item in self._dados:
            if item.get(campo) == valor:
                return item
        return None

    def tamanho(self):
        return len(self._dados)

    def buscar_por_nome(self, nome):
        resultado = []
        for p in self._dados:
            if nome.lower() in p["nome"].lower():
                resultado.append(p)
        return resultado

    def ordenar_por_nome(self):
        self._dados.sort(key=lambda p: p["nome"].lower())

    def ordenar_por_preco(self):
        self._dados.sort(key=lambda p: p["preco"])
