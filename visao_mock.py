import cv2
import os
import logging

# Logger para no de visao
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [NO DE VISAO] - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def detectar_obstaculo(caminho_imagem):
    """
    Simula o no de visao de um robo movel (como o Turtlebot).
    Na vida real, este script carregaria um modelo YOLO/PyTorch embarcado.
    """
    # 1. Verifica se a imagem existe (simulando a leitura da camera do robo)
    if not os.path.exists(caminho_imagem):
        logger.error(f"Falha no sensor: Imagem '{caminho_imagem}' nao encontrada.")
        raise FileNotFoundError(f"Imagem {caminho_imagem} nao encontrada.")
    
    # Lemos a matriz da imagem com OpenCV
    imagem = cv2.imread(caminho_imagem)
    logger.info("Frame do sensor capturado e lido com sucesso.")
    
    # Simulacao:
    arquivo_pesos = "pesos_modelo.txt"
    grau_confianca = 0.95  # Padrao: modelo excelente (95% de certeza)
    
    if os.path.exists(arquivo_pesos):
        with open(arquivo_pesos, 'r') as f:
            pesos_atuais = f.read().strip()
            
            # Tenta converter o valor lido para float
            try:
                valor_peso = int(pesos_atuais)

                # Se o peso for menor que 8, a precisao cai
                if valor_peso < 8:
                    grau_confianca = 0.35  # Simula um modelo degradado/cego
                    logger.warning(f"ALERTA: O modelo carregou com pesos corrompidos ou degradados (peso atual: {valor_peso}).")
            except ValueError:
                logger.error(f"Erro: O arquivo de pesos contém um valor inválido que não é um número inteiro: '{pesos_atuais}'")
                grau_confianca = 0.35 # Assume falha de seguranca se o formato estiver errado

    else:
        logger.warning(f"Arquivo '{arquivo_pesos}' nao encontrado. Operando com confianca padrao.")
    
    # O modelo retorna o que "viu"
    logger.info(f"Analise concluida. Obstaculo detectado com {grau_confianca * 100:.1f}% de confianca.")
    
    # Lógica de navegação baseada na visão
    acao_recomendada = "PARAR" if grau_confianca >= 0.80 else "AVANCAR"
    
    if acao_recomendada == "PARAR": logger.info("Comando de navegação enviado: PARAR (obstaculo perto).")
    else: logger.error("Comando de navegação enviado: AVANÇAR (risco extremo de colisao fisica).")
    
    return {
        "classe_objeto": "parede",
        "confianca": grau_confianca,
        "acao_recomendada": acao_recomendada
    }

if __name__ == "__main__":
    pasta_dados = "data"
    caminho_teste = os.path.join(pasta_dados, "obstaculo.jpg")
    
    # Cria uma imagem falsa so p testar o script
    if not os.path.exists(caminho_teste):
        os.makedirs(pasta_dados, exist_ok=True)
        with open(caminho_teste, "w") as f:
            f.write("imagem_fake")
            
    logger.info("Iniciando teste de inicializacao do robo...")
    resultado = detectar_obstaculo(caminho_teste)
    logger.info(f"Resultado final do no: {resultado}")