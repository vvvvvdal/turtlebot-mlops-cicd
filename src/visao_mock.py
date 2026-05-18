import cv2
import os

# grau de confianca do modelo (de 0.0 a 1.0)
CONFIANCA_BOA  = 0.95  # modelo com pesos bons
CONFIANCA_RUIM = 0.35  # modelo com pesos ruins

def detectar_obstaculo(caminho_imagem):
    # verifica se a imagem existe
    if not os.path.exists(caminho_imagem):
        print(f"[Visao] ERRO: imagem '{caminho_imagem}' nao encontrada")
        raise FileNotFoundError(f"imagem {caminho_imagem} nao existe")

    # le a imagem com opencv (na vida real seria uma camera)
    imagem = cv2.imread(caminho_imagem)
    print("[Visao] imagem lida com sucesso")

    # verifica o arquivo de pesos do modelo
    confianca = CONFIANCA_BOA  # assume bom por padrao
    arquivo_pesos = "pesos_modelo.txt"

    if os.path.exists(arquivo_pesos):
        with open(arquivo_pesos, "r") as f:
            conteudo = f.read().strip()
        try:
            peso = int(conteudo)
            if peso < 8:
                confianca = CONFIANCA_RUIM
                print(f"[Visao] pesos ruins detectados (peso={peso}), confianca baixa!")
        except:
            confianca = CONFIANCA_RUIM
            print("[Visao] arquivo de pesos com formato invalido")
    else:
        print("[Visao] arquivo de pesos nao encontrado, usando padrao")

    print(f"[Visao] confianca do modelo: {confianca * 100:.0f}%")

    # decide a acao baseado na confianca
    if confianca >= 0.80:
        acao = "PARAR"
    else:
        acao = "AVANCAR"

    return {"confianca": confianca, "acao_recomendada": acao}


if __name__ == "__main__":
    # cria uma imagem de teste
    os.makedirs("data", exist_ok=True)
    with open("data/obstaculo.jpg", "w") as f:
        f.write("imagem_fake")

    resultado = detectar_obstaculo("data/obstaculo.jpg")
    print("resultado:", resultado)