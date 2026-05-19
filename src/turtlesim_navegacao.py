import sys
import time
import subprocess
import rclpy

from geometry_msgs.msg import Twist

from navegacao_node import NavegacaoTurtlesim
from turtlesim_constantes import JANELA_ALTURA, JANELA_LARGURA

def iniciar_turtlesim():
    return subprocess.Popen([
        "ros2", "run", "turtlesim", "turtlesim_node",
        "--ros-args",
        "-p", f"width:={JANELA_LARGURA}",
        "-p", f"height:={JANELA_ALTURA}",
    ])

def pedir_peso():
    # Lendo o peso do arquivo peso.txt (usado no CI/CD)
    try:
        with open("models/peso.txt") as f:
            conteudo = f.read().strip()
        peso = int(conteudo)
        if not 1 <= peso <= 10:
            raise ValueError(f"Peso fora do intervalo de 1 a 10: {peso}")
        print(f"Peso lido de models/peso.txt: {peso}")
        return peso
    except FileNotFoundError:
        pass  # arquivo não existe, cai no input abaixo

    # Lendo o peso via terminal
    print("Rode o turtlesim em outro terminal: ros2 run turtlesim turtlesim_node\n")
    while True:
        entrada = input("Digite o peso do modelo (de 1 a 10): ")
        try:
            peso = int(entrada)
            if 1 <= peso <= 10:
                return peso
            print("O valor deve estar entre 1 e 10. Tente novamente.\n")
        except ValueError:
            print("Entrada invalida. Você precisa digitar um numero inteiro de 1 a 10.\n")


def main():
    peso = pedir_peso()

    print(f"\nIniciando Turtlebot com peso: {peso}")

    processo_turtlesim = iniciar_turtlesim()
    time.sleep(2)  # aguarda o nó subir

    rclpy.init()
    node = NavegacaoTurtlesim(peso)

    aprovado = False
    try:
        node.desenhar_mapa()
        time.sleep(0.5)
        aprovado = node.navegar()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
    finally:
        node.pub_vel.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()
        processo_turtlesim.terminate()

    sys.exit(0 if aprovado else 1)


if __name__ == "__main__":
    main()
