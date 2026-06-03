class Pilha:
    def __init__(self):
        self._dados = []

    def empilhar(self, elemento):
        self._dados.append(elemento)

    def desempilhar(self):
        if not self.esta_vazia():
            return self._dados.pop()
        return None

    def topo(self):
        if not self.esta_vazia():
            return self._dados[-1]
        return None

    def esta_vazia(self):
        return len(self._dados) == 0