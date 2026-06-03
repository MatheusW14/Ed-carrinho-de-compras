class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self._cabeca = None

    def inserir(self, dado):
        novo = No(dado)
        novo.proximo = self._cabeca
        self._cabeca = novo

    def listar(self):
        resultado = []
        atual = self._cabeca
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def esta_vazia(self):
        return self._cabeca is None