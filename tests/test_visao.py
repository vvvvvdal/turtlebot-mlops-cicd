import os
import pytest
import logging
from visao_mock import detectar_obstaculo

# Logger para o teste
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [TESTE CI/CD] - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_seguranca_colisao():
    """
    Este teste simula a barreira de CI/CD. 
    Garante que o robo não vai bater no mundo fisico validando se o modelo 
    detecta a parede com alta confianca e manda o comando de PARAR.
    """
    logger.info("Iniciando a bateria de testes de segurança de visão...")
    caminho_imagem = "data/obstaculo.jpg"
    
    # Prepara o ambiente criando a imagem falsa caso o GitHub Actions rode do zero
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(caminho_imagem):
        with open(caminho_imagem, "w") as f:
            f.write("imagem_fake_simulando_parede")
        logger.info(f"Imagem de teste mockada criada em: {caminho_imagem}")

    # Executa a inferencia
    logger.info("Acionando o no de visao para avaliar o cenario de obstaculo...")
    resultado = detectar_obstaculo(caminho_imagem)

    # Coletando os resultados para o log
    confianca_obtida = resultado["confianca"]
    acao_obtida = resultado["acao_recomendada"]
    
    logger.info(f"Avaliação do Modelo: Confiança: {confianca_obtida*100:.1f}%, Acao decidida: {acao_obtida}")

    # TESTE 1: A IA tem certeza do que esta vendo? (Minimo 80% de confiança)
    if confianca_obtida < 0.80:
        logger.error(f"Falha de segurança. O modelo não está confiante o suficiente para operar ({confianca_obtida*100:.1f}%).")
        
    assert confianca_obtida >= 0.80, \
        f"FALHA CRITICA. Confiança muito baixa ({confianca_obtida * 100}%). Risco de colisão."
    
    logger.info("Etapa 1 (Confiança): APROVADA.")

    # TESTE 2: A decisão tomada pela IA é segura?
    if acao_obtida != "PARAR":
        logger.error(f"Risco iminente de colisao. O modelo mandou o robô {acao_obtida} contra uma parede.")
        
    assert acao_obtida == "PARAR", \
        f"FALHA DE SEGURANÇA. O robo decidiu {acao_obtida} contra o obstaculo"
        
    logger.info("Etapa 2 (Decisão de navegação): APROVADA. Deploy seguro liberado.")