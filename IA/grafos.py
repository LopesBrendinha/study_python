class Aresta:
    def __init__(self, nome: str, peso: float, destino: "Vertice"):
        self.nome = nome
        self.peso = peso
        self.destino = destino

    def __str__(self):
        return f"Aresta(nome={self.nome}, peso={self.peso}, destino={self.destino.nome})"


class Vertice:
    def __init__(self, nome: str):
        self.nome = nome
        self.arestas = []

    def adicionar_aresta(self, nome: str, peso: float, destino: "Vertice"):
        aresta = Aresta(nome, peso, destino)
        self.arestas.append(aresta)

    def listar_arestas(self):
        print(f"Vértice {self.nome}:")

        if not self.arestas:
            print("  Sem arestas")
            return

        for aresta in self.arestas:
            print(
                f"  --[{aresta.nome}, peso={aresta.peso}]--> {aresta.destino.nome}"
            )

    def __str__(self):
        return self.nome

class Grafo:
    def __init__(self):
        self.vertices = []

    def adicionar_vertice(self, nome: str):
        vertice = Vertice(nome)
        self.vertices.append(vertice)
        return vertice

    def listar_grafo(self):
        for vertice in self.vertices:
            vertice.listar_arestas()
            print()



# Criando o grafo
grafo = Grafo()

# Criando os vértices
a = grafo.adicionar_vertice("A")
b = grafo.adicionar_vertice("B")
c = grafo.adicionar_vertice("C")

# Criando as arestas
a.adicionar_aresta("A para B", 10, b)
a.adicionar_aresta("A para C", 5, c)
b.adicionar_aresta("B para C", 2, c)
c.adicionar_aresta("C para A", 7, a)

# Exibindo o grafo
grafo.listar_grafo()