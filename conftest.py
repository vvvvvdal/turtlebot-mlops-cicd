import logging

def pytest_configure():
    # Silenciar os logs verbosos de bibliotecas de terceiros (HTTP e Ollama)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("ollama").setLevel(logging.WARNING)
