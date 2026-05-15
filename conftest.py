import logging

def pytest_configure():
    # Silenciar os logs verbosos de bibliotecas de terceiros (HTTP e Gemini)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google_genai").setLevel(logging.WARNING)
