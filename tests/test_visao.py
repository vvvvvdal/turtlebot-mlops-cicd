import os
import pytest
from visao_mock import detectar_obstaculo

def test_modelo_detecta_obstaculo_com_confianca():
    # cria a imagem de teste
    os.makedirs("data", exist_ok=True)
    caminho = "data/obstaculo.jpg"
    if not os.path.exists(caminho):
        with open(caminho, "w") as f:
            f.write("imagem_fake")

    resultado = detectar_obstaculo(caminho)

    confianca = resultado["confianca"]
    acao = resultado["acao_recomendada"]
    print(f"confianca={confianca*100:.0f}% acao={acao}")

    # o modelo tem que estar confiante (acima de 80%)
    assert confianca >= 0.80, f"confianca muito baixa: {confianca*100:.0f}%. robo pode colidir!"

    # e tem que mandar parar (detectou obstaculo)
    assert acao == "PARAR", f"modelo mandou '{acao}' em vez de PARAR. risco de colisao!"