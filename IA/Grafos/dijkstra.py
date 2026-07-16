import tkinter as tk
from tkinter import ttk, messagebox
import heapq


# =====================================
# CLASSE ARESTA
# =====================================
class Aresta:

    def __init__(self, nome, peso, destino):
        self.nome = nome
        self.peso = float(peso)
        self.destino = destino


# =====================================
# CLASSE VÉRTICE
# =====================================
class Vertice:

    def __init__(self, nome):
        self.nome = nome.upper()
        self.arestas = []

    # Adiciona uma aresta ao vértice
    def adicionar_aresta(self, nome, peso, destino):
        self.arestas.append(Aresta(nome, peso, destino))

    def __str__(self):
        return self.nome


# =====================================
# CLASSE GRAFO
# =====================================
class Grafo:

    def __init__(self):
        self.vertices = []

    # Adiciona um novo vértice
    def adicionar_vertice(self, nome):

        if self.buscar_vertice(nome):
            return

        self.vertices.append(Vertice(nome))

    # Procura um vértice pelo nome
    def buscar_vertice(self, nome):

        nome = nome.upper()

        for vertice in self.vertices:

            if vertice.nome == nome:
                return vertice

        return None

    def adicionar_aresta(self, origem_nome, destino_nome, peso):

        origem = self.buscar_vertice(origem_nome)
        destino = self.buscar_vertice(destino_nome)

        if origem is None or destino is None:
            return False

        origem.adicionar_aresta(
            f"{origem.nome}-{destino.nome}",
            peso,
            destino
        )

        destino.adicionar_aresta(
            f"{destino.nome}-{origem.nome}",
            peso,
            origem
        )

        return True

    # Algoritmo de Dijkstra
    def dijkstra(self, origem_nome, destino_nome):

        origem = self.buscar_vertice(origem_nome)
        destino = self.buscar_vertice(destino_nome)

        if origem is None or destino is None:
            return None, None

        # Inicializa as distâncias
        distancias = {}
        anteriores = {}

        for v in self.vertices:
            distancias[v] = float("inf")
            anteriores[v] = None

        distancias[origem] = 0

        # Fila de prioridade
        fila = []
        heapq.heappush(
            fila,
            (0, origem.nome, origem)
        )

        while fila:

            distancia_atual, _, vertice_atual = heapq.heappop(fila)

            if distancia_atual > distancias[vertice_atual]:
                continue

            for aresta in vertice_atual.arestas:

                vizinho = aresta.destino

                nova_distancia = (
                    distancia_atual + aresta.peso
                )

                if nova_distancia < distancias[vizinho]:

                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = vertice_atual

                    heapq.heappush(
                        fila,
                        (
                            nova_distancia,
                            vizinho.nome,
                            vizinho
                        )
                    )

        if distancias[destino] == float("inf"):
            return None, None

        caminho = []

        atual = destino

        while atual is not None:
            caminho.append(atual.nome)
            atual = anteriores[atual]

        caminho.reverse()

        return caminho, distancias[destino]


# =====================================
# CRIA O GRAFO
# =====================================

grafo = Grafo()

# =====================================
# INTERFACE GRÁFICA
# =====================================

# Cria a janela principal
janela = tk.Tk()
janela.title("Grafo - Algoritmo de Dijkstra")
janela.geometry("900x750")
janela.resizable(False, False)


# ========= TÍTULO =========
titulo = tk.Label(
    janela,
    text="Grafo Ponderado Não Direcionado",
    font=("Arial", 18, "bold")
)
titulo.pack(pady=10)


# =====================================
# FRAME PARA ADICIONAR VÉRTICE
# =====================================

frame_vertice = tk.LabelFrame(
    janela,
    text="Adicionar Vértice",
    padx=10,
    pady=10
)
frame_vertice.pack(fill="x", padx=15, pady=5)

tk.Label(
    frame_vertice,
    text="Nome:"
).grid(row=0, column=0, padx=5)

entry_vertice = tk.Entry(frame_vertice, width=10)
entry_vertice.grid(row=0, column=1, padx=5)

btn_add_vertice = tk.Button(
    frame_vertice,
    text="Adicionar"
)
btn_add_vertice.grid(row=0, column=2, padx=10)


# =====================================
# FRAME PARA ADICIONAR ARESTA
# =====================================

frame_aresta = tk.LabelFrame(
    janela,
    text="Adicionar Aresta",
    padx=10,
    pady=10
)
frame_aresta.pack(fill="x", padx=15, pady=5)

tk.Label(frame_aresta, text="Origem").grid(row=0, column=0)

combo_origem = ttk.Combobox(
    frame_aresta,
    width=10,
    state="readonly"
)
combo_origem.grid(row=0, column=1, padx=5)

tk.Label(frame_aresta, text="Destino").grid(row=0, column=2)

combo_destino = ttk.Combobox(
    frame_aresta,
    width=10,
    state="readonly"
)
combo_destino.grid(row=0, column=3, padx=5)

tk.Label(frame_aresta, text="Peso").grid(row=0, column=4)

entry_peso = tk.Entry(frame_aresta, width=8)
entry_peso.grid(row=0, column=5, padx=5)

btn_add_aresta = tk.Button(
    frame_aresta,
    text="Adicionar Aresta"
)
btn_add_aresta.grid(row=0, column=6, padx=10)


# =====================================
# FRAME PARA CALCULAR O MENOR CAMINHO
# =====================================

frame_dijkstra = tk.LabelFrame(
    janela,
    text="Menor Caminho",
    padx=10,
    pady=10
)
frame_dijkstra.pack(fill="x", padx=15, pady=5)

tk.Label(frame_dijkstra, text="Origem").grid(row=0, column=0)

combo_inicio = ttk.Combobox(
    frame_dijkstra,
    width=10,
    state="readonly"
)
combo_inicio.grid(row=0, column=1, padx=5)

tk.Label(frame_dijkstra, text="Destino").grid(row=0, column=2)

combo_fim = ttk.Combobox(
    frame_dijkstra,
    width=10,
    state="readonly"
)
combo_fim.grid(row=0, column=3, padx=5)

btn_calcular = tk.Button(
    frame_dijkstra,
    text="Calcular Menor Caminho"
)
btn_calcular.grid(row=0, column=4, padx=15)


# =====================================
# FRAME DAS LISTAS
# =====================================

frame_listas = tk.Frame(janela)
frame_listas.pack(fill="both", expand=True, padx=15, pady=10)


# Lista de vértices
frame_vertices = tk.LabelFrame(
    frame_listas,
    text="Vértices"
)
frame_vertices.pack(side="left", fill="both", expand=True, padx=5)

lista_vertices = tk.Listbox(
    frame_vertices,
    width=25,
    height=15
)
lista_vertices.pack(fill="both", expand=True)


# Lista de arestas
frame_arestas = tk.LabelFrame(
    frame_listas,
    text="Arestas"
)
frame_arestas.pack(side="left", fill="both", expand=True, padx=5)

lista_arestas = tk.Listbox(
    frame_arestas,
    width=45,
    height=15
)
lista_arestas.pack(fill="both", expand=True)


# =====================================
# RESULTADO
# =====================================

resultado = tk.Label(
    janela,
    text="",
    font=("Arial", 12, "bold"),
    fg="blue",
    justify="left",
    wraplength=750,   # Quebra a linha automaticamente
    anchor="w"
)

resultado.pack(pady=10)
# =====================================
# FUNÇÕES DA INTERFACE
# =====================================

# Atualiza as Combobox com os vértices cadastrados
def atualizar_comboboxes():

    nomes = [v.nome for v in grafo.vertices]

    combo_origem["values"] = nomes
    combo_destino["values"] = nomes

    combo_inicio["values"] = nomes
    combo_fim["values"] = nomes


# Atualiza as listas de vértices e arestas
def atualizar_listas():

    lista_vertices.delete(0, tk.END)
    lista_arestas.delete(0, tk.END)

    # Lista de vértices
    for vertice in grafo.vertices:
        lista_vertices.insert(tk.END, vertice.nome)

    # Lista de arestas
    adicionadas = set()

    for vertice in grafo.vertices:

        for aresta in vertice.arestas:

            origem = vertice.nome
            destino = aresta.destino.nome

            # Evita mostrar duas vezes a mesma aresta
            chave = tuple(sorted([origem, destino]))

            if chave not in adicionadas:

                adicionadas.add(chave)

                lista_arestas.insert(
                    tk.END,
                    f"{origem} <-> {destino}   Peso: {aresta.peso}"
                )


# =====================================
# BOTÃO ADICIONAR VÉRTICE
# =====================================

def adicionar_vertice():

    nome = entry_vertice.get().strip().upper()

    if nome == "":
        messagebox.showwarning(
            "Aviso",
            "Digite um nome para o vértice."
        )
        return

    if grafo.buscar_vertice(nome):
        messagebox.showwarning(
            "Aviso",
            "Esse vértice já existe."
        )
        return

    grafo.adicionar_vertice(nome)

    entry_vertice.delete(0, tk.END)

    atualizar_comboboxes()
    atualizar_listas()


# =====================================
# BOTÃO ADICIONAR ARESTA
# =====================================

def adicionar_aresta():

    origem = combo_origem.get()
    destino = combo_destino.get()
    peso = entry_peso.get()

    if origem == "" or destino == "" or peso == "":

        messagebox.showwarning(
            "Aviso",
            "Preencha todos os campos."
        )

        return

    try:
        peso = float(peso)

    except ValueError:

        messagebox.showerror(
            "Erro",
            "Peso inválido."
        )

        return

    grafo.adicionar_aresta(
        origem,
        destino,
        peso
    )

    entry_peso.delete(0, tk.END)

    atualizar_listas()


# =====================================
# BOTÃO CALCULAR
# =====================================

def calcular():

    origem = combo_inicio.get()
    destino = combo_fim.get()

    if origem == "" or destino == "":

        messagebox.showwarning(
            "Aviso",
            "Selecione origem e destino."
        )

        return

    caminho, distancia = grafo.dijkstra(
        origem,
        destino
    )

    if caminho is None:

        resultado.config(
            text="Não existe caminho entre os vértices."
        )

    else:

        resultado.config(
            text=f"Menor caminho:\n{' -> '.join(caminho)}\n\nDistância Total: {distancia}"
        )


# =====================================
# LIGA OS BOTÕES ÀS FUNÇÕES
# =====================================

btn_add_vertice.config(
    command=adicionar_vertice
)

btn_add_aresta.config(
    command=adicionar_aresta
)

btn_calcular.config(
    command=calcular
)


# =====================================
# INICIA O PROGRAMA
# =====================================

janela.mainloop()