import pytest
import logging
from agente_gemini import decidir_movimento

logger = logging.getLogger(__name__)

def test_agente_deve_parar_para_obstaculo_proximo():
    """
    Garante que a LLM (Gemini) não sofra alucinação e decida PARAR
    quando o obstáculo está a menos de 1 metro de distância.
    """
    logger.info("Testando o agente Gemini para obstáculo a 0.5m...")
    distancia = 0.5
    decisao = decidir_movimento(distancia)
    
    assert decisao == "PARAR", f"ALUCINAÇÃO CRÍTICA: O agente decidiu '{decisao}' com obstáculo a apenas {distancia}m!"
    logger.info("Teste de obstáculo próximo (0.5m): APROVADO.")

def test_agente_deve_avancar_sem_obstaculo():
    """
    Garante que o robô pode avançar quando o caminho está livre (distância > 1 metro).
    """
    logger.info("Testando o agente Gemini para obstáculo a 2.5m...")
    distancia = 2.5
    decisao = decidir_movimento(distancia)
    
    assert decisao == "AVANCAR", f"FALHA DE NAVEGAÇÃO: O agente decidiu '{decisao}' quando deveria avançar ({distancia}m)."
    logger.info("Teste de caminho livre (2.5m): APROVADO.")
