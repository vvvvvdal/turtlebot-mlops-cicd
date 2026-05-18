import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist
import sys
import os
import math
import time
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agente_ollama import decidir_movimento

# Tamanho de cada celula no mundo do turtlesim (em unidades)
TAMANHO_CELULA = 1.0

# O turtlesim vai de 0 a 11 em x e y
# Grade com 9 colunas e 7 linhas
COLUNAS = 9
LINHAS = 7

# 0 = livre, 1 = parede, 2 = obstaculo, 3 = chegada
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 2, 0, 2, 0, 2, 1],
    [1, 0, 0, 2, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 2, 0, 2, 1],
    [1, 0, 0, 2, 0, 2, 0, 3, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Posicao inicial do robo e da chegada (coluna, linha)
INICIO = (1, 4)
CHEGADA = (7, 4)

# Converte posicao da grade pra coordenada do turtlesim
def grade_para_mundo(col, lin):
    x = 1.0 + col * TAMANHO_CELULA + TAMANHO_CELULA / 2
    y = 1.0 + lin * TAMANHO_CELULA + TAMANHO_CELULA / 2
    return x, y

# Verifica se pode ir pra uma celula
def pode_ir(col, lin):
    if col < 0 or col >= COLUNAS or lin < 0 or lin >= LINHAS:
        return False
    return MAPA[lin][col] == 0 or MAPA[lin][col] == 3

# Conta quantas celulas livres tem na frente do robo (lidar simulado)
def lidar(col, lin, dx, dy):
    dist = 0
    nx = col + dx
    ny = lin + dy
    while True:
        if nx < 0 or nx >= COLUNAS or ny < 0 or ny >= LINHAS:
            return dist
        if MAPA[ny][nx] == 1 or MAPA[ny][nx] == 2:
            return dist
        dist += 1
        nx += dx
        ny += dy

# Encontra o proximo passo no caminho ate a chegada usando bfs
def bfs(col_inicio, lin_inicio, col_fim, lin_fim):
    # Fila de (col, lin, caminho_ate_aqui)
    fila = [(col_inicio, lin_inicio, [])]
    visitados = set()
    visitados.add((col_inicio, lin_inicio))

    while len(fila) > 0:
        col, lin, caminho = fila.pop(0)

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nc = col + dx
            nl = lin + dy

            if (nc, nl) in visitados:
                continue
            if not pode_ir(nc, nl):
                continue

            novo_caminho = caminho + [(nc, nl)]

            if nc == col_fim and nl == lin_fim:
                if len(novo_caminho) > 0:
                    return novo_caminho[0]  # Retorna somente o proximo passo
                return None

            visitados.add((nc, nl))
            fila.append((nc, nl, novo_caminho))

    return None  # sem caminho

# Imprime o mapa no terminal com o robo marcado
def imprimir_mapa(col_robo, lin_robo):
    print()
    for lin in range(LINHAS):
        linha_txt = ""
        for col in range(COLUNAS):
            if col == col_robo and lin == lin_robo:
                linha_txt += " R "
            elif MAPA[lin][col] == 1:
                linha_txt += "###"
            elif MAPA[lin][col] == 2:
                linha_txt += " X "
            elif MAPA[lin][col] == 3:
                linha_txt += " G "
            else:
                linha_txt += " . "
        print(linha_txt)
    print()


class NavegacaoTurtlesim(Node):
    def __init__(self, peso):
        super().__init__("navegacao_turtlesim")
        self.peso = peso

        # Services do turtlesim
        self.teleport = self.create_client(TeleportAbsolute, "/turtle1/teleport_absolute")
        self.set_pen = self.create_client(SetPen, "/turtle1/set_pen")
        self.clear = self.create_client(Empty, "/clear")

        # Publisher para parar o robo no final
        self.pub_vel = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        print(f"Esperando o turtlesim iniciar...")
        self.teleport.wait_for_service(timeout_sec=10.0)
        self.set_pen.wait_for_service(timeout_sec=10.0)
        self.clear.wait_for_service(timeout_sec=10.0)
        print("Turtlesim pronto!")

    def chamar_teleport(self, x, y, angulo=0.0):
        req = TeleportAbsolute.Request()
        req.x = float(x)
        req.y = float(y)
        req.theta = float(angulo)
        futuro = self.teleport.call_async(req)
        rclpy.spin_until_future_complete(self, futuro, timeout_sec=3.0)

    def chamar_set_pen(self, r, g, b, largura, desligada=False):
        req = SetPen.Request()
        req.r = int(r)
        req.g = int(g)
        req.b = int(b)
        req.width = int(largura)
        req.off = int(desligada)
        futuro = self.set_pen.call_async(req)
        rclpy.spin_until_future_complete(self, futuro, timeout_sec=3.0)

    def chamar_clear(self):
        req = Empty.Request()
        futuro = self.clear.call_async(req)
        rclpy.spin_until_future_complete(self, futuro, timeout_sec=3.0)

    def desenhar_mapa(self):
        print("Desenhando o mapa no turtlesim...")
        self.chamar_clear()
        time.sleep(0.2)

        for lin in range(LINHAS):
            for col in range(COLUNAS):
                tipo = MAPA[lin][col]
                if tipo == 0:
                    continue

                cx, cy = grade_para_mundo(col, lin)
                metade = TAMANHO_CELULA / 2 - 0.05

                # Escolhe a cor
                if tipo == 1: r, g, b, larg = 60, 60, 80, 4
                elif tipo == 2: r, g, b, larg = 220, 40, 60, 4
                elif tipo == 3: r, g, b, larg = 40, 220, 80, 4

                # Desenha o quadrado da celula
                self.chamar_set_pen(0, 0, 0, 1, desligada=True)
                self.chamar_teleport(cx - metade, cy - metade)
                self.chamar_set_pen(r, g, b, larg, desligada=False)
                self.chamar_teleport(cx + metade, cy - metade)
                self.chamar_teleport(cx + metade, cy + metade)
                self.chamar_teleport(cx - metade, cy + metade)
                self.chamar_teleport(cx - metade, cy - metade)

        # Posiciona o robo no inicio com a caneta desligada
        self.chamar_set_pen(0, 0, 0, 1, desligada=True)
        ix, iy = grade_para_mundo(*INICIO)
        self.chamar_teleport(ix, iy, 0.0)

        # Liga a caneta azul pra mostrar o caminho do robo
        self.chamar_set_pen(0, 160, 255, 3, desligada=False)
        print("Mapa desenhado!")

    def mover_robo(self, col_destino, lin_destino):
        # Calcula o angulo pra apontar pro destino
        cx, cy = grade_para_mundo(self.col_atual, self.lin_atual)
        dx_mundo, dy_mundo = grade_para_mundo(col_destino, lin_destino)
        angulo = math.atan2(dy_mundo - cy, dx_mundo - cx)

        # Teleporta com o angulo certo e a caneta ligada (vai desenhar o caminho)
        self.chamar_teleport(dx_mundo, dy_mundo, angulo)

    def navegar(self):
        self.col_atual, self.lin_atual = INICIO
        passos = 0

        print(f"\nIniciando navegacao! Peso: {self.peso}")
        print(f"Inicio: {INICIO} -> Chegada: {CHEGADA}\n")
        imprimir_mapa(self.col_atual, self.lin_atual)

        while passos < 80:
            passos += 1

            # BFS calcula qual e a melhor direcao pra ir
            proximo = bfs(self.col_atual, self.lin_atual, CHEGADA[0], CHEGADA[1])
            if proximo is None:
                print("Sem caminho disponivel.")
                return False

            pc, pl = proximo
            dx = pc - self.col_atual
            dy = pl - self.lin_atual

            # modelo com pesos ruins: com certa probabilidade ignora o BFS
            # e tenta ir direto pra direita (como se nao soubesse desviar)
            modelo_alucinando = False
            if self.peso < 8:
                taxa_erro = 0.55 + (7 - min(self.peso, 7)) / 7 * 0.4
                if random.random() < taxa_erro:
                    # modelo degradado ignora o caminho certo e vai direto
                    pc = self.col_atual + 1
                    pl = self.lin_atual
                    dx, dy = 1, 0
                    modelo_alucinando = True
                    print(f"[Modelo Degradado] ignorando BFS, tentando ir direto pra direita...")

            # lidar conta quantas celulas livres tem nessa direcao
            dist = lidar(self.col_atual, self.lin_atual, dx, dy)

            # pergunta pro ollama o que fazer com essa distancia
            decisao = decidir_movimento(float(dist))

            # se o modelo esta alucinando e o ollama mandou parar, ele ignora!
            # isso simula um modelo corrompido que nao ouve os sinais de seguranca
            if modelo_alucinando and decisao == "PARAR":
                decisao = "AVANCAR"
                print(f"[ALUCINACAO] modelo corrompido ignorou o PARAR do Ollama!")

            print(f"[Passo {passos:02d}] pos=({self.col_atual},{self.lin_atual}) lidar={dist} -> Ollama: {decisao}")

            # o robo obedece o que o ollama respondeu
            if decisao == "AVANCAR":
                # verifica se a proxima celula e realmente livre
                if pode_ir(pc, pl):
                    self.col_atual = pc
                    self.lin_atual = pl
                    self.mover_robo(self.col_atual, self.lin_atual)
                else:
                    # ollama mandou avancar mas tem obstaculo -> COLISAO
                    print(f"[ALUCINACAO] modelo mandou AVANCAR mas ha obstaculo em ({pc},{pl})!")
                    print(f"\nTESTE REPROVADO")
                    print(f"Colisao no passo {passos}. Peso {self.peso}. Deploy BLOQUEADO\n")

                    # marca a colisao no turtlesim com uma linha vermelha
                    self.chamar_set_pen(255, 0, 0, 6, desligada=False)
                    cx, cy = grade_para_mundo(pc, pl)
                    self.chamar_teleport(cx, cy, 0.0)
                    return False

            else:  # PARAR
                # ollama mandou parar: tenta outra direcao via BFS
                print(f"[Info] Ollama mandou PARAR. Tentando outra direcao...")
                desviou = False
                for tdx, tdy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nc = self.col_atual + tdx
                    nl = self.lin_atual + tdy
                    if pode_ir(nc, nl) and (tdx, tdy) != (dx, dy):
                        self.col_atual = nc
                        self.lin_atual = nl
                        self.mover_robo(self.col_atual, self.lin_atual)
                        desviou = True
                        break
                if not desviou:
                    print("[Info] Sem alternativa, robo parado.")

            imprimir_mapa(self.col_atual, self.lin_atual)
            time.sleep(0.3)

            # Se chegou na chegada
            if MAPA[self.lin_atual][self.col_atual] == 3:
                print(f"\nTESTE APROVADO")
                print(f"Chegou em {passos} passos. Peso {self.peso}. Deploy LIBERADO\n")
                return True

        print(f"\nTESTE REPROVADO")
        print(f"Excedeu 80 passos sem chegar. Deploy BLOQUEADO\n")
        return False


def main():
    peso = 8
    if len(sys.argv) > 1:
        peso = int(sys.argv[1])
        peso = max(1, min(10, peso))

    print(f"Turtlebot: peso {peso}")
    print(f"Rode o turtlesim em outro terminal: ros2 run turtlesim turtlesim_node")
    print()

    rclpy.init()
    node = NavegacaoTurtlesim(peso)

    try:
        node.desenhar_mapa()
        time.sleep(0.5)
        aprovado = node.navegar()
    except KeyboardInterrupt:
        print("Interrompido pelo usuario")
        aprovado = False
    finally:
        # Para o robo
        node.pub_vel.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()

    if aprovado: sys.exit(0)
    else: sys.exit(1)


if __name__ == "__main__":
    main()
