class Pilha:
    """
    Classe Pilha
    Esta classe implementa uma estrutura de dados do tipo pilha (LIFO - Last In, First Out).
    Permite adicionar elementos ao topo da pilha, remover o elemento do topo e verificar o estado da pilha.
    Métodos:
    ---------
    - __init__():
        Inicializa uma nova instância da classe Pilha.
    - empilhar(elemento):
        Adiciona um elemento ao topo da pilha.
    - desempilhar():
        Remove e retorna o elemento do topo da pilha. Retorna None se a pilha estiver vazia.
    - topo():
        Retorna o elemento no topo da pilha sem removê-lo. Retorna None se a pilha estiver vazia.
    - esta_vazia():
        Verifica se a pilha está vazia. Retorna True se estiver vazia, caso contrário, retorna False.
    """

    def __init__(self):
        self._dados = []

    def empilhar(self, elemento):
        """
        Adiciona um elemento ao topo da pilha.

        Args:
            elemento: O elemento a ser adicionado à pilha.
        """
        self._dados.append(elemento)

    def desempilhar(self):
        """
        Remove e retorna o elemento do topo da pilha.

        Retorna:
            O elemento do topo da pilha, se a pilha não estiver vazia.
            None, se a pilha estiver vazia.
        """
        if not self.esta_vazia():
            return self._dados.pop()
        return None

    def topo(self):
        """
        Retorna o elemento no topo da pilha sem removê-lo.

        Retorna:
            O elemento no topo da pilha, se a pilha não estiver vazia.
            None, se a pilha estiver vazia.
        """
        if not self.esta_vazia():
            return self._dados[-1]
        return None

    def esta_vazia(self):
        """
        Verifica se a pilha está vazia.

        Retorna:
            bool: True se a pilha estiver vazia, caso contrário, False.
        """
        return len(self._dados) == 0
