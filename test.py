from bs4 import BeautifulSoup
import requests

main_url = 'https://sites.google.com/view/movilidadmorelos/oriente/ruta-1-oriente'
response = requests.get(main_url)

if response.status_code == 200:

    html = response.text

    # Parsear el HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Buscar el <span> con las clases específicas
    links = soup.find_all('a')
    for link in links:
        if link.get('class') == ['XqQF9c']:
            print(link.get('href'))
    
    

