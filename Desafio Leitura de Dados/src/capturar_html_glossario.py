import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z"
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), '..', 'data/glossario', 'letras_links.json')

#Identificar os links de cada letra do glossário

def pegar_links_letras():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()  # dispara um erro se status != 200
    
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na requisição: {e}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')

    letras = {}
    for a in soup.select('a[href^="https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/"]'):
        texto = a.text.strip().upper()
        href = a['href'].strip()
        if len(texto) == 1 and texto.isalpha():
            letras[texto] = href

    # Salva em JSON
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(letras, f, ensure_ascii=False, indent=2)

    print(f"[OK] Links salvos em {CAMINHO_ARQUIVO}")

    return letras

# Teste rápido
if __name__ == "__main__":
    letras = pegar_links_letras()
    for letra, link in sorted(letras.items()):
        print(f"{letra} -> {link}")