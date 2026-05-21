import ollama

# Distancia 0 = obstaculo na proxima celula (PERIGOSO)
# Distancia > 0 = tem pelo menos uma celula livre (SEGURO)
DISTANCIA_PAREDE = 0

INSTRUCAO_SISTEMA = (
    "You are a Turtlebot safety system. "
    "You must respond with ONLY one word. "
    "If the situation is DANGEROUS, answer: PARAR. "
    "If the situation is SAFE, answer: AVANCAR. "
    "Never explain. Never add other words. Just one word."
)

def decidir_movimento(distancia: int) -> str:

    if distancia <= DISTANCIA_PAREDE: situacao = "DANGEROUS"
    else: situacao = "SAFE"

    prompt = f"Current situation: {situacao}. What is your decision?"

    print(f"[OLLAMA] Distancia: {distancia} celulas. Situacao: {situacao}")

    try:
        resposta = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[
                {"role": "system", "content": INSTRUCAO_SISTEMA},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.0}
        )
        texto = resposta["message"]["content"].strip().upper()
        print(f"[OLLAMA] resposta: {texto}")

        # procura pela palavra de decisao na resposta
        if "PARAR" in texto: return "PARAR"
        elif "AVANCAR" in texto: return "AVANCAR"
        else:
            print("[OLLAMA] resposta inesperada, assumindo PARAR por seguranca")
            return "PARAR"

    except Exception as erro:
        print(f"[OLLAMA] erro: {erro}")
        return "PARAR"  # Se der erro, para por seguranca


if __name__ == "__main__":
    print("Testando o agente Ollama...")
    print("Com obstaculo (0 celulas):", decidir_movimento(0))
    print("Sem obstaculo (3 celulas):", decidir_movimento(3))