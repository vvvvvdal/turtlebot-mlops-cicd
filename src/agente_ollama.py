import ollama
import concurrent.futures
import re
import logging

logger = logging.getLogger("agente_ollama")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("ollama_agent.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

DISTANCIA_SEGURA = 1.0

INSTRUCAO_SISTEMA = (
    "You are a Turtlebot safety system. "
    "You must respond with ONLY one word. "
    "If the situation is DANGEROUS, answer: PARAR. "
    "If the situation is SAFE, answer: AVANCAR. "
    "Never explain. Never add other words. Just one word."
)

def decidir_movimento(distancia):

    if distancia <= DISTANCIA_SEGURA: situacao = "DANGEROUS"
    else: situacao = "SAFE"

    prompt = f"Current situation: {situacao}. What is your decision?"

    logger.info(f"[Ollama] Distancia: {distancia} celulas. Situacao: {situacao}")
    print(f"[Ollama] Distancia: {distancia} celulas. Situacao: {situacao}")

    try:
        def fazer_chamada():
            return ollama.chat(
                model="qwen2.5:1.5b",
                messages=[
                    {"role": "system", "content": INSTRUCAO_SISTEMA},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.0}
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(fazer_chamada)
            try:
                resposta = future.result(timeout=1.5)
            except concurrent.futures.TimeoutError:
                logger.warning("[Ollama] Timeout de 1.5s excedido! Assumindo PARAR por seguranca.")
                print("[Ollama] Timeout de 1.5s excedido! Assumindo PARAR por seguranca.")
                return "PARAR"

        texto = resposta["message"]["content"].strip().upper()
        logger.info(f"[Ollama] resposta original: {texto}")
        print(f"[Ollama] resposta original: {texto}")

        # extraindo as palavras com regex
        match = re.search(r'\b(PARAR|AVANCAR)\b', texto)
        if match:
            comando = match.group(1)
            logger.info(f"[Ollama] comando sanitizado: {comando}")
            return comando
        else:
            logger.warning("[Ollama] resposta inesperada, assumindo PARAR por seguranca")
            print("[Ollama] resposta inesperada, assumindo PARAR por seguranca")
            return "PARAR"

    except Exception as erro:
        logger.error(f"[Ollama] erro: {erro}")
        print(f"[Ollama] erro: {erro}")
        return "PARAR"  # Se der erro, para por seguranca


if __name__ == "__main__":
    print("Testando o agente Ollama...")
    print("Com obstaculo (0 celulas):", decidir_movimento(0))
    print("Sem obstaculo (3 celulas):", decidir_movimento(3))