# Tamanho de cada célula no mundo do turtlesim (em unidades)
TAMANHO_CELULA = 1

# O turtlesim vai de 0 a 11 em x e y
# Grade com 11 colunas e 7 linhas
COLUNAS = 11
LINHAS = 7

# 0 = livre, 1 = parede, 2 = obstáculo, 3 = chegada
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 2, 0, 2, 0, 2, 0, 0, 1],
    [1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 2, 0, 0, 1],
    [1, 0, 0, 2, 0, 2, 0, 2, 0, 3, 1],
    [1, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Posição inicial do robô e da chegada (coluna, linha)
INICIO = (1, 4)
CHEGADA = (9, 4)


# Tamanho da janela do turtlesim
JANELA_LARGURA = 800
JANELA_ALTURA = 800

def grade_para_mundo(col, lin):
    """Converte posição da grade para coordenada do turtlesim."""
    x = col * TAMANHO_CELULA + TAMANHO_CELULA / 2
    y = (LINHAS - 1 - lin) * TAMANHO_CELULA + TAMANHO_CELULA / 2
    return x, y


def pode_ir(col, lin):
    """Verifica se é possível mover para uma célula."""
    if col < 0 or col >= COLUNAS or lin < 0 or lin >= LINHAS:
        return False
    return MAPA[lin][col] == 0 or MAPA[lin][col] == 3


def lidar(col, lin, dx, dy):
    """Conta quantas células livres existem à frente do robô (LiDAR simulado)."""
    dist = 0
    nx, ny = col + dx, lin + dy
    while True:
        if nx < 0 or nx >= COLUNAS or ny < 0 or ny >= LINHAS:
            return dist
        if MAPA[ny][nx] in (1, 2):
            return dist
        dist += 1
        nx += dx
        ny += dy


def bfs(col_inicio, lin_inicio, col_fim, lin_fim):
    """
    Encontra o próximo passo no caminho até a chegada usando BFS.
    Retorna apenas o próximo passo (col, lin), ou None se não houver caminho.
    """
    fila = [(col_inicio, lin_inicio, [])]
    visitados = {(col_inicio, lin_inicio)}

    while fila:
        col, lin, caminho = fila.pop(0)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nc, nl = col + dx, lin + dy

            if (nc, nl) in visitados or not pode_ir(nc, nl):
                continue

            novo_caminho = caminho + [(nc, nl)]

            if nc == col_fim and nl == lin_fim:
                return novo_caminho[0] if novo_caminho else None

            visitados.add((nc, nl))
            fila.append((nc, nl, novo_caminho))

    return None


def imprimir_mapa(col_robo, lin_robo):
    simbolos = {1: "###", 2: " X ", 3: " C ", 0: " . "}
    print()
    for lin in range(LINHAS - 1, -1, -1):
        linha_txt = ""
        for col in range(COLUNAS):
            if col == col_robo and lin == lin_robo:
                linha_txt += " T "
            else:
                linha_txt += simbolos[MAPA[lin][col]]
        print(linha_txt)
    print()
