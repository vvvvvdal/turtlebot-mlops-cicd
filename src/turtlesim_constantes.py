# Tamanho de cada célula no mundo do turtlesim (em unidades)
TAMANHO_CELULA = 1.0

# O turtlesim vai de 0 a 11 em x e y
# Grade com 11 colunas e 7 linhas
COLUNAS = 11
LINHAS = 7

# 0 = livre, 1 = parede, 2 = obstáculo, 3 = chegada
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 2, 0, 2, 0, 2, 0, 0, 1],
    [1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 2, 0, 3, 1],
    [1, 0, 0, 2, 0, 2, 0, 2, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Posição inicial do robô e da chegada (coluna, linha)
INICIO = (1, 4)
CHEGADA = (9, 3)
