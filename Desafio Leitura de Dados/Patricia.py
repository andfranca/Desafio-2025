#importando as bibliotecas necessárias
import requests
import bs4
import pandas as pd
from bs4 import BeautifulSoup
#fazendo a requisição para o site
url = 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z'
resposta = requests.get(url)
#verificando o status da requisição
if resposta.status_code == 200:
    print('Requisição bem sucedida!')
else:
    print('Erro na requisição:', resposta.status_code)
#fazendo o parse do conteúdo HTML
soup = BeautifulSoup(resposta.text, 'html.parser')
#criando uma lista para armazenar os links
lista_links = []
#buscar todos os links na página
conteudo = soup.find_all('div', class_='card.little-cards')
"extrair os links,adcionar à lista e printar os links"
for link in conteudo:
    link = link.find('a')['class']
    lista_links.append(link)
for link in lista_links:
    print(lista_links)
#criando um dataframe para armazenar os links
df = pd.DataFrame(lista_links, columns=['Links'])







        

