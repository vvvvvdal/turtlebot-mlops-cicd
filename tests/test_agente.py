import pytest
from agente_ollama import decidir_movimento

# testa se o agente para quando o obstaculo ta perto
def test_parar_com_obstaculo_perto():
    distancia = 0.5  # 0.5 metros, bem perto
    decisao = decidir_movimento(distancia)
    print(f"distancia={distancia}m -> decisao={decisao}")
    assert decisao == "PARAR", f"esperava PARAR mas got '{decisao}' com obstaculo a {distancia}m"

# testa se o agente avanca quando o caminho ta livre
def test_avancar_com_caminho_livre():
    distancia = 2.5  # 2.5 metros, bem longe
    decisao = decidir_movimento(distancia)
    print(f"distancia={distancia}m -> decisao={decisao}")
    assert decisao == "AVANCAR", f"esperava AVANCAR mas got '{decisao}' com {distancia}m de distancia"
