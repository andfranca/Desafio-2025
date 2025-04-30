import requests
from bs4 import BeautifulSoup
import json
import os
from time import sleep

# Caminhos dos arquivos
PASTA_GLOSSARIO = os.path.join(os.path.dirname(__file__), '..', 'data', 'glossario')
CAMINHO_LETRAS = os.path.join(PASTA_GLOSSARIO, 'letras_links.json')

#Carregar os links de letras do arquivo JSON
def carregar_links_letras():
    with open(CAMINHO_LETRAS, 'r', encoding='utf-8') as f:
        return json.load(f)
    
#Ler cada letra e extrair os links 
def extrair_termos_da_letra(letra, url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Letra {letra} - {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    termos = []
    for link in soup.select('a[href^="https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/"]'):
        texto = link.text.strip()
        href = link.get('href')
        if texto and href and f"/{letra.lower()}/" in href:
            termos.append({
                'titulo': texto,
                'url': href
            })

    return termos

#Salvar cada letra em um arquivo JSON separado
def salvar_termos_letra(letra, termos):
    caminho_arquivo = os.path.join(PASTA_GLOSSARIO, f"{letra.lower()}.json")
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(termos, f, ensure_ascii=False, indent=2)
    print(f"[OK] Letra {letra} salva com {len(termos)} termos.")


# Juntar tudo e processar todas as letras
def processar_todas_as_letras():
    letras = carregar_links_letras()
    for letra, url in sorted(letras.items()):
        termos = extrair_termos_da_letra(letra, url)
        salvar_termos_letra(letra, termos)
        sleep(1)  # espera 1 segundo para evitar sobrecarga

#Teste rápido
if __name__ == "__main__":
    processar_todas_as_letras()