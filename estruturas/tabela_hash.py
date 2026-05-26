class TabelaHash:
    def __init__(self, tamanho=10):
        self._tamanho = tamanho
        self._tabela = [[] for _ in range(tamanho)]

    def _hash(self, chave):
        return chave % self._tamanho

    def inserir(self, chave, valor):
        indice = self._hash(chave)
        for i, (k, v) in enumerate(self._tabela[indice]):
            if k == chave:
                self._tabela[indice][i] = (chave, valor)
                return
        self._tabela[indice].append((chave, valor))

    def buscar(self, chave):
        indice = self._hash(chave)
        for k, v in self._tabela[indice]:
            if k == chave:
                return v
        return None

    def remover(self, chave):
        indice = self._hash(chave)
        self._tabela[indice] = [(k, v) for k, v in self._tabela[indice] if k != chave]
