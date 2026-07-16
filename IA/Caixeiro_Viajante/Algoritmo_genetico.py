import math


class Ponto:
    """
    Representa um ponto do Problema do Caixeiro Viajante.
    """

    def __init__(self, identificador: int, x: float, y: float):
        self.identificador = identificador
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """
        Define como o objeto será exibido ao ser impresso.
        """
        return (
            f"Ponto(id={self.identificador}, "
            f"x={self.x}, y={self.y})"
        )


class MatrizDistancias:
    """
    Responsável por calcular e armazenar as distâncias
    entre todos os pontos do problema.

    A matriz evita que a mesma distância seja calculada
    várias vezes durante a execução do algoritmo.
    """

    def __init__(self, pontos: list[Ponto]):
        self.pontos = pontos
        self.matriz = self._criar_matriz()

    def _calcular_distancia(self, ponto_a: Ponto, ponto_b: Ponto) -> int:
        """
        Calcula a distância euclidiana entre dois pontos.
        """

        diferenca_x = ponto_a.x - ponto_b.x
        diferenca_y = ponto_a.y - ponto_b.y

        distancia = math.sqrt(
            diferenca_x ** 2 + diferenca_y ** 2
        )

        return round(distancia)

    def _criar_matriz(self) -> list[list[int]]:
        """
        Cria a matriz contendo as distâncias entre
        todos os pares de pontos.
        """

        quantidade_pontos = len(self.pontos)

        matriz = [
            [0] * quantidade_pontos
            for _ in range(quantidade_pontos)
        ]

        for i in range(quantidade_pontos):
            for j in range(i + 1, quantidade_pontos):

                distancia = self._calcular_distancia(
                    self.pontos[i],
                    self.pontos[j]
                )

                # A distância de A até B é igual à de B até A.
                matriz[i][j] = distancia
                matriz[j][i] = distancia

        return matriz

class LeitorArquivo:
    """
    Responsável por ler o arquivo de entrada no formato TSPLIB.

    A classe identifica as informações do cabeçalho e lê as
    coordenadas presentes após a seção NODE_COORD_SECTION.
    """

    def __init__(self, caminho_arquivo: str):
        # Caminho do arquivo que será lido.
        self.caminho_arquivo = caminho_arquivo

        # Informações que serão obtidas do cabeçalho do arquivo.
        self.nome = ""
        self.comentario = ""
        self.tipo = ""
        self.dimensao = 0
        self.tipo_peso_aresta = ""

        # Lista que armazenará os objetos da classe Ponto.
        self.pontos = []

    def ler(self) -> list[Ponto]:
        """
        Lê o arquivo de entrada e retorna uma lista de objetos Ponto.
        """

        # Abre o arquivo em modo de leitura.
        with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:

            # Indica se o programa já chegou à seção das coordenadas.
            lendo_coordenadas = False

            # Percorre o arquivo linha por linha.
            for linha in arquivo:

                # Remove espaços e quebras de linha do início e do final.
                linha = linha.strip()

                # Ignora linhas vazias.
                if not linha:
                    continue

                # Verifica o início da seção que contém as coordenadas.
                if linha == "NODE_COORD_SECTION":
                    lendo_coordenadas = True
                    continue

                # Quando estiver na seção de coordenadas, cria os pontos.
                if lendo_coordenadas:

                    # Alguns arquivos TSPLIB terminam com a palavra EOF.
                    if linha == "EOF":
                        break

                    partes = linha.split()

                    identificador = int(partes[0])
                    coordenada_x = float(partes[1])
                    coordenada_y = float(partes[2])

                    ponto = Ponto(
                        identificador,
                        coordenada_x,
                        coordenada_y
                    )

                    self.pontos.append(ponto)

                # Antes da seção de coordenadas, lê o cabeçalho.
                else:
                    self._ler_cabecalho(linha)

        return self.pontos

    def _ler_cabecalho(self, linha: str) -> None:
        """
        Interpreta uma linha do cabeçalho do arquivo TSPLIB.
        """

        # Separa a chave do valor utilizando o primeiro ":" encontrado.
        chave, valor = linha.split(":", 1)

        chave = chave.strip()
        valor = valor.strip()

        if chave == "NAME":
            self.nome = valor

        elif chave == "COMMENT":
            self.comentario = valor

        elif chave == "TYPE":
            self.tipo = valor

        elif chave == "DIMENSION":
            self.dimensao = int(valor)

        elif chave == "EDGE_WEIGHT_TYPE":
            self.tipo_peso_aresta = valor

def ler_rota(caminho_arquivo: str) -> list[int]:
    """
    Lê a sequência de pontos após TOUR_SECTION.
    """

    rota = []
    lendo_rota = False

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if linha == "TOUR_SECTION":
                lendo_rota = True
                continue

            if lendo_rota:
                if linha in ("-1", "EOF"):
                    break

                rota.append(int(linha))

    return rota

# 1. Lê os pontos do arquivo
leitor = LeitorArquivo("entrada/entrada.txt")
pontos = leitor.ler()

# 2. Cria a matriz de distâncias
matriz_distancias = MatrizDistancias(pontos)

# 3. Lê a rota conhecida
rota = ler_rota("entrada/melhor_rota.txt")

# 4. Calcula a distância total da rota
distancia_total = 0

for i in range(len(rota)):
    ponto_atual = rota[i] - 1
    proximo_ponto = rota[(i + 1) % len(rota)] - 1

    distancia_total += matriz_distancias.matriz[ponto_atual][proximo_ponto]

print("Distância da rota:", distancia_total)