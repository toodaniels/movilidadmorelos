import requests
from bs4 import BeautifulSoup

# URL de la página web
url = "https://sites.google.com/view/movilidadmorelos/oriente/ruta-1-oriente"

# Hacer la solicitud
response = requests.get(url)


print(response.status_code)

if response.status_code == 200:
    # Analizar el HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar el iframe del mapa
    iframe = soup.find_all('iframe')

    # muestra el enlace de cada mapa en la pagina
    for iframe_tag in iframe:
        src = iframe_tag['src']
        label = iframe_tag['aria-label'].replace('Map, ', '')
        route_code, route_title = label.split('.-')        
        map_id =  src.replace('https://www.google.com/maps/d/embed?mid=', '')
        print(f"Mapa ID: {map_id}")
        print(route_code, route_title)

        
# else:
#     print(f"Error al acceder a la página. Código de estado: {response.status_code}")

zones = [
    'CENTRO',
    'SUR',
    'ORIENTE'
]