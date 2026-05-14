import google.generativeai as genai
import logging
import os
from dotenv import load_dotenv
from config_gemini import INSTRUCAO_SISTEMA, CONFIG_MODELO

# Logs do Gemini
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [IA-GEMINI] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carrega as variaveis do arquivo .env
load_dotenv()

# Puxa a chave que o dotenv carregou
CHAVE_API = os.environ.get("GEMINI_API_KEY")

if not CHAVE_API:
    logger.error("Chave da API nao encontrada. Verifique o arquivo .env ou as Secrets do GitHub.")
    exit(1)

# Configura a chave da API
genai.configure(api_key=CHAVE_API)

def decidir_movimento(distancia_obstaculo):
    """
    Recebe a distancia do sensor LiDAR e consulta o Gemini para decidir a acao.
    """
    logger.info(f"Leitura do LiDAR: Obstaculo detectado a {distancia_obstaculo}m.")
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=INSTRUCAO_SISTEMA
    )

    prompt = f"O sensor LiDAR indica um objeto a {distancia_obstaculo} metros a frente. O que eu devo fazer?"
    
    try:
        response = model.generate_content(prompt, generation_config=CONFIG_MODELO)
        decisao = response.text.strip().upper()
        
        if "PARAR" in decisao: decisao = "PARAR"
        elif "AVANCAR" in decisao: decisao = "AVANCAR"
        
        logger.info(f"Decisão da IA: {decisao}")
        return decisao
    except Exception as e:
        logger.error(f"Erro na API do Gemini: {e}")
        return "PARAR" # Em caso de erro, por segurança, o robo para

if __name__ == "__main__":
    # Teste rápido manual
    print("Testando Turtlebot autônomo:")
    distancia = 0.5 # Simulando obstaculo perto
    print(f"Decisao final para {distancia}m: {decidir_movimento(distancia)}")