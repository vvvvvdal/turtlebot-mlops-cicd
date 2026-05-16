import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import threading
import time
import os
import math

from agente_ollama import decidir_movimento
from visao_mock import detectar_obstaculo

VELOCIDADE_PADRAO = 0.15
VELOCIDADE_NULA = 0.0

class MLOpsTurtlebotNode(Node):
    def __init__(self):
        super().__init__('mlops_turtlebot_node')
        
        self.get_logger().info('Iniciando no ROS 2 de MLOps para o Turtlebot...')
        
        # Publisher para os motores do robo
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscriber para o LiDAR (sensor de distancia)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Variaveis de estado
        self.distancia_frente = 10.0  # Comeca com um valor seguro
        self.comando_atual = "PARAR"  # Comeca parado, por seguranca
        
        # Cria a imagem falsa para a visao se nao existir
        self.caminho_imagem = "data/obstaculo.jpg"
        if not os.path.exists(self.caminho_imagem):
            os.makedirs("data", exist_ok=True)
            with open(self.caminho_imagem, "w") as f:
                f.write("imagem_fake")
                
        # Thread separada para consultar a IA e Visao sem travar o loop de controle do ROS 2
        self.ia_thread = threading.Thread(target=self.loop_de_decisao_ia)
        self.ia_thread.daemon = True
        self.ia_thread.start()
        
        # Timer para enviar os comandos de velocidade continuamente (10Hz)
        self.create_timer(0.1, self.publish_velocity)

    def scan_callback(self, msg):
        """ Callback do LiDAR: Pega a distancia dos obstaculos bem a frente do robo """
        ranges = msg.ranges
        num_leituras = len(ranges)
        
        if num_leituras == 0:
            return
            
        # Pega as leituras na frente (cone de 30 graus: 15 graus pra cada lado do indice 0)
        ang_index_esq = 15
        ang_index_dir = num_leituras - 15
        
        frente_ranges = []
        for i in range(ang_index_esq):
            if not math.isinf(ranges[i]) and not math.isnan(ranges[i]) and ranges[i] > 0.0:
                frente_ranges.append(ranges[i])
                
        for i in range(ang_index_dir, num_leituras):
            if not math.isinf(ranges[i]) and not math.isnan(ranges[i]) and ranges[i] > 0.0:
                frente_ranges.append(ranges[i])
                
        if frente_ranges:
            self.distancia_frente = min(frente_ranges)
        else:
            self.distancia_frente = 10.0 # Sem obstaculo
            
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

    def publish_velocity(self):
        """ Publica a velocidade de fato nos motores """
        twist = Twist()
        
        if self.comando_atual == "AVANCAR":
            twist.linear.x = VELOCIDADE_PADRAO # 15 cm/s
            twist.angular.z = VELOCIDADE_NULA
        else:
            twist.linear.x = VELOCIDADE_NULA
            twist.angular.z = VELOCIDADE_NULA
            
        self.cmd_vel_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = MLOpsTurtlebotNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
