import sys
import time

import rclpy
from geometry_msgs.msg import Twist

from navegacao_node import NavegacaoTurtlesim


def pedir_peso():
    """Solicita ao usuário um peso de modelo válido (1–10)."""
    print("Rode o turtlesim em outro terminal: ros2 run turtlesim turtlesim_node\n")
    while True:
        entrada = input("Digite o peso do modelo (de 1 a 10): ")
        try:
            peso = int(entrada)
            if 1 <= peso <= 10:
                return peso
            print("O valor deve estar entre 1 e 10. Tente novamente.\n")
        except ValueError:
            print("Entrada inválida. Você precisa digitar um número inteiro de 1 a 10.\n")


def main():
    peso = pedir_peso()
    print(f"\nIniciando Turtlebot com peso: {peso}")

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

    sys.exit(0 if aprovado else 1)


if __name__ == "__main__":
    main()
