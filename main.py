import requests
from bs4 import BeautifulSoup

main_url = 'https://sites.google.com/view/movilidadmorelos'

def find_all(path, element_filter, class_filter=None):
    url = f'{main_url}/{path}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all(element_filter, class_=class_filter)
    else:
        print(f"Error al acceder a la página. Código de estado: {response.status_code}")
        return []

def get_map_ids():

    iframes = find_all('oriente/ruta-1-oriente', 'iframe')

    # muestra el enlace de cada mapa en la pagina
    for iframe_tag in iframes:
        src = iframe_tag['src']
        label = iframe_tag['aria-label'].replace('Map, ', '')
        route_code, route_title = label.split('.-')        
        map_id =  src.replace('https://www.google.com/maps/d/embed?mid=', '')
        print(f"Mapa ID: {map_id}")
        print(route_code, route_title)

def get_routes():
    routes = find_all('oriente/ruta-1-oriente', element_filter='a', class_filter='XqQF9c')

    for route_tag in routes:
        href = route_tag['href']
        print(href)

if __name__ == '__main__':
    get_map_ids()
    get_routes()

