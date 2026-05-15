import ollama
import logging

# Configuracoes do modelo
INSTRUCAO_SISTEMA = "Você é um robô. Regra de Segurança: Se a distância for MAIOR que 100 centímetros, responda APENAS 'AVANCAR'. Se a distância for MENOR OU IGUAL a 100 centímetros, responda APENAS 'PARAR'."
CONFIG_MODELO = {
    "temperature": 0.0,
    "top_p": 1.0,
}

# Logs da IA Local
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [IA-LOCAL] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def decidir_movimento(distancia_obstaculo):
    """
    Recebe a distancia do sensor LiDAR e consulta o modelo local (Ollama) para decidir a acao.
    """
    logger.info(f"Leitura do LiDAR: Obstaculo detectado a {distancia_obstaculo}m.")
    estado_risco = "PERIGOSA" if distancia_obstaculo <= 1.0 else "SEGURA"
    prompt_completo = f"Situação: {estado_risco}.\nRegra: Se a situação for PERIGOSA, responda PARAR. Se for SEGURA, responda AVANCAR.\nDecisão:"
    
    try:
        response = ollama.chat(
            model='qwen2.5:1.5b',
            messages=[
                {'role': 'user', 'content': prompt_completo}
            ],
            options={
                'temperature': CONFIG_MODELO.get("temperature", 0.1), # Temperatura baixa p evitar criatividade/alucinações
                'top_p': CONFIG_MODELO.get("top_p", 1.0)
            }
        )
        decisao = response['message']['content'].strip().upper()
        logger.info(f"Resposta crua do modelo: {decisao}") # As vezes ele pode responder com frases como "Decisão: PARAR" ou "Decisão: AVANCAR", por isso precisamos fazer o tratamento abaixo.
        
        if "PARAR" in decisao: decisao = "PARAR"
        elif "AVANCAR" in decisao: decisao = "AVANCAR"
        
        logger.info(f"Decisao da IA Local: {decisao}")
        return decisao
    except Exception as e:
        logger.error(f"Erro no Ollama local: {e}")
        return "PARAR" # Em caso de erro, por seguranca, o robo para

if __name__ == "__main__":
    # Teste rapido manual
    print("Testando Turtlebot autonomo:")
    distancia = 0.5 # Simulando obstaculo perto
    print(f"Decisao final para {distancia}m: {decidir_movimento(distancia)}")