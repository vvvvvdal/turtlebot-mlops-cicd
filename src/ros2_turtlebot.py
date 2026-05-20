import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import threading
import time
import os
import math

os.environ["QT_LOGGING_RULES"] = "*.warning=false"

from ollama_agente import decidir_movimento
from visao_mock import detectar_obstaculo

POSICAO_MIN = 0.0
POSICAO_MAX = 11.0

VELOCIDADE_PADRAO = 1.0
VELOCIDADE_NULA = 0.0
VELOCIDADE_GIRO = 0.8

class TurtlebotNode(Node):
    def __init__(self):
        super().__init__('turtlebot_node')
        
        self.get_logger().info('Iniciando no ROS 2 para o Turtlebot...')
        
        # Publisher para os motores do robo
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Subscriber para o Turtlesim (simulando sensor de distancia)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # Variaveis de estado
        self.distancia_frente = 10.0  # Comeca com um valor seguro
        self.comando_atual = "PARAR"  # Comeca parado, por seguranca
        
        # Cria a imagem falsa para a visao se nao existir
        self.caminho_imagem = "data/imagem_teste.jpg"
        if not os.path.exists(self.caminho_imagem):
            os.makedirs("data", exist_ok=True)
            with open(self.caminho_imagem, "w") as f:
                f.write("imagem_teste.jpg")
                
        # Thread separada para consultar a IA e Visao sem travar o loop de controle do ROS 2
        self.ia_thread = threading.Thread(target=self.loop_de_decisao_ia)
        self.ia_thread.daemon = True
        self.ia_thread.start()
        
        # Timer para enviar os comandos de velocidade continuamente (10Hz)
        self.create_timer(0.1, self.publish_velocidade)

    def pose_callback(self, msg):
        """ Callback do Turtlesim: Simula o LiDAR calculando a distância para as paredes do mapa (11x11) """
        x = msg.x
        y = msg.y
        theta = msg.theta
        
        distancias = []
        # O mapa do Turtlesim vai de 0 a 11 em x e y
        if math.cos(theta) > 0.001: distancias.append((POSICAO_MAX - x) / math.cos(theta))
        elif math.cos(theta) < -0.001: distancias.append((POSICAO_MIN - x) / math.cos(theta))
            
        if math.sin(theta) > 0.001: distancias.append((POSICAO_MAX - y) / math.sin(theta))
        elif math.sin(theta) < -0.001: distancias.append((POSICAO_MIN - y) / math.sin(theta))
            
        if distancias: self.distancia_frente = min(distancias)
        else: self.distancia_frente = 10.0
            
    def loop_de_decisao_ia(self):
        """ Rodando loop a cada 3 segundos """
        # Espera o ROS 2 iniciar corretamente antes da primeira chamada
        time.sleep(2.0)
        
        while rclpy.ok():
            try:
                # 1. Primeiro consulta o modelo de visao (mock)
                self.get_logger().info('Consultando modelo de Visao Computacional...')
                resultado_visao = detectar_obstaculo(self.caminho_imagem)
                
                if resultado_visao["acao_recomendada"] == "PARAR":
                    self.get_logger().warning('Visao mandou PARAR. Seguranca ativada.')
                    self.comando_atual = "PARAR"
                else:
                    # 2. Visao liberou, agora pergunta ao LLM Local (Ollama)
                    self.get_logger().info(f'Visao ok. Consultando Ollama (distancia={self.distancia_frente:.2f}m)...')
                    decisao_llm = decidir_movimento(round(self.distancia_frente, 2))
                    
                    self.get_logger().info(f'Ollama decidiu: {decisao_llm}')
                    self.comando_atual = decisao_llm
            except Exception as e:
                self.get_logger().error(f'Erro na tomada de decisao: {e}')
                self.comando_atual = "PARAR" # Falha segura: em caso de erro, o robo para.
                
            time.sleep(3.0)

    def publish_velocidade(self):
        """ Publica a velocidade de fato nos motores """
        twist = Twist()
        
        if self.comando_atual == "AVANCAR":
            twist.linear.x = VELOCIDADE_PADRAO # 1.0 m/s
            twist.angular.z = VELOCIDADE_NULA
        else:
            twist.linear.x = VELOCIDADE_NULA
            # Gira o robo para mudar de direcao quando encontra a parede
            twist.angular.z = VELOCIDADE_GIRO # 0.8 rad/s
            
        self.cmd_vel_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
