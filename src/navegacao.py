import math
import time
import random

import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist

from mapa import MAPA, INICIO, CHEGADA, grade_para_mundo, pode_ir, lidar, bfs, imprimir_mapa
from ollama_agente import decidir_movimento


class NavegacaoTurtlesim(Node):
    def __init__(self, peso: int) -> None:
        super().__init__("navegacao_turtlesim")
        self.peso = peso

        self.teleport = self.create_client(TeleportAbsolute, "/turtle1/teleport_absolute")
        self.set_pen = self.create_client(SetPen, "/turtle1/set_pen")
        self.clear = self.create_client(Empty, "/clear")
        self.pub_vel = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        print("Esperando o turtlesim iniciar...")
        self.teleport.wait_for_service(timeout_sec=10.0)
        self.set_pen.wait_for_service(timeout_sec=10.0)
        self.clear.wait_for_service(timeout_sec=10.0)
        print("Turtlesim pronto!")


    def chamar_teleport(self, x: float, y: float, angulo=0.0) -> None:
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = float(x), float(y), float(angulo)
        rclpy.spin_until_future_complete(self, self.teleport.call_async(req), timeout_sec=3.0)

    def chamar_set_pen(self, r: int, g: int, b: int, largura: int, desligada: bool = False) -> None:
        req = SetPen.Request()
        req.r, req.g, req.b = int(r), int(g), int(b)
        req.width, req.off = int(largura), int(desligada)
        rclpy.spin_until_future_complete(self, self.set_pen.call_async(req), timeout_sec=3.0)

    def chamar_clear(self) -> None:
        rclpy.spin_until_future_complete(self, self.clear.call_async(Empty.Request()), timeout_sec=3.0)


    def desenhar_mapa(self) -> None:
        print("Desenhando o mapa no turtlesim...")
        self.chamar_clear()
        time.sleep(0.2)

        cores = {
            1: (60, 60, 80, 4),
            2: (220, 40, 60, 4),
            3: (40, 220, 80, 4),
        }

        for lin, linha in enumerate(MAPA):
            for col, tipo in enumerate(linha):
                if tipo == 0:
                    continue
                cx, cy = grade_para_mundo(col, lin)
                metade = 0.5 - 0.05  # TAMANHO_CELULA / 2 - margem
                r, g, b, larg = cores[tipo]

                self.chamar_set_pen(0, 0, 0, 1, desligada=True)
                self.chamar_teleport(cx - metade, cy - metade)
                self.chamar_set_pen(r, g, b, larg, desligada=False)
                self.chamar_teleport(cx + metade, cy - metade)
                self.chamar_teleport(cx + metade, cy + metade)
                self.chamar_teleport(cx - metade, cy + metade)
                self.chamar_teleport(cx - metade, cy - metade)

        self.chamar_set_pen(0, 0, 0, 1, desligada=True)
        ix, iy = grade_para_mundo(*INICIO)
        self.chamar_teleport(ix, iy, 0.0)
        self.chamar_set_pen(0, 160, 255, 3, desligada=False)
        print("Mapa desenhado.")

    def mover_robo(self, col_destino: int, lin_destino: int) -> None:
        cx, cy = grade_para_mundo(self.col_atual, self.lin_atual)
        dx_mundo, dy_mundo = grade_para_mundo(col_destino, lin_destino)
        angulo = math.atan2(dy_mundo - cy, dx_mundo - cx)
        self.chamar_teleport(dx_mundo, dy_mundo, angulo)


    def modelo_alucinando(self):
        """Retorna True se o modelo degradado decide ignorar o BFS neste passo."""
        if self.peso >= 8:
            return False
        taxa_erro = 0.55 + (7 - min(self.peso, 7)) / 7 * 0.4
        return random.random() < taxa_erro

    def reprovar(self, motivo: str, passos: int) -> None:
        print(f"\nTESTE REPROVADO")
        print(f"{motivo} Passo {passos}. Peso {self.peso}. Deploy bloqueado\n")

    def navegar(self) -> bool:
        self.col_atual, self.lin_atual = INICIO
        passos = 0

        print(f"\nIniciando navegação! Peso: {self.peso}")
        print(f"Início: {INICIO} -> Chegada: {CHEGADA}\n")
        imprimir_mapa(self.col_atual, self.lin_atual)

        while passos < 80:
            passos += 1

            proximo = bfs(self.col_atual, self.lin_atual, CHEGADA[0], CHEGADA[1])
            if proximo is None:
                print("Sem caminho disponivel.")
                return False

            pc, pl = proximo
            dx, dy = pc - self.col_atual, pl - self.lin_atual

            alucinando = self.modelo_alucinando()
            if alucinando:
                pc, pl, dx, dy = self.col_atual + 1, self.lin_atual, 1, 0
                print("[OLLAMA] alucinacao. ignorando BFS, tentando ir direto para a direita...")

            dist = lidar(self.col_atual, self.lin_atual, dx, dy)
            decisao = decidir_movimento(dist)

            if alucinando and decisao == "PARAR":
                decisao = "AVANCAR"
                print("[OLLAMA] alucinacao. modelo corrompido ignorou o PARAR")

            print(f"[Passo {passos:02d}] pos=({self.col_atual},{self.lin_atual}) lidar={dist} -> Ollama: {decisao}")

            if decisao == "AVANCAR":
                if pode_ir(pc, pl):
                    self.col_atual, self.lin_atual = pc, pl
                    self.mover_robo(self.col_atual, self.lin_atual)
                else:
                    print(f"[OLLAMA] alucinacao. modelo mandou AVANCAR mas ha obstaculo em ({pc},{pl}).")
                    self.reprovar(f"Bateu na parede.", passos)
                    self.chamar_set_pen(255, 0, 0, 6, desligada=False)
                    cx, cy = grade_para_mundo(pc, pl)
                    self.chamar_teleport(cx, cy, 0.0)
                    return False
            else:
                print("[INFO] Ollama mandou PARAR. Tentando outra direção...")
                desviou = False
                for tdx, tdy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nc, nl = self.col_atual + tdx, self.lin_atual + tdy
                    if pode_ir(nc, nl) and (tdx, tdy) != (dx, dy):
                        self.col_atual, self.lin_atual = nc, nl
                        self.mover_robo(self.col_atual, self.lin_atual)
                        desviou = True
                        break
                if not desviou:
                    print("[INFO] Sem alternativa, robo parado.")

            imprimir_mapa(self.col_atual, self.lin_atual)
            time.sleep(0.3)

            if MAPA[self.lin_atual][self.col_atual] == 3:
                print(f"\nTESTE APROVADO")
                print(f"Chegou no fim com {passos} passos. Peso {self.peso}. Deploy Liberado\n")
                return True

        self.reprovar("Chegou em 80 passos e não chegou no fim.", passos)
        return False
