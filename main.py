import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import numpy as np
from bs4 import BeautifulSoup
import re


main_url = "https://sites.google.com/view/movilidadmorelos"

zones = [
    { 'id': 'CENTRO', 'name': 'Centro', 'path': 'centro'},
    # { 'id': 'SUR', 'name': 'Sur', 'path': 'sur'},
    # { 'id': 'ORIENTE', 'name': 'Oriente', 'path': 'oriente'},
    # { 'id': 'RUTA_DE_LA_SALUD', 'name': 'Ruta de salud', 'path': 'ruta-de-la-salud'}
]

def parse_text(text):
    match = re.match(r"^(\d+)\.\s*(.+)$", text)  # Buscar número antes del punto
    if match:
        code, name = match.groups()
    else:
        code, name = "1", text.strip()  # Si no hay número, asignar "1" a code

    return code, name

def get_iframe_data(iframe_tag):
    src = iframe_tag['src']
    label = iframe_tag['aria-label'].replace('Map, ', '')
    route_code, route_title = parse_text(label)

    map_id = src.replace(
        'https://www.google.com/maps/d/embed?mid=', '')
    return {
        'code': route_code,
        'title': route_title,
        'map_id': map_id
    }
    

def get_maps(url):
    print(f'Obteniendo iframe de {url}')
    # Hacer la solicitud
    response = requests.get(url)
    if response.status_code == 200:
        # Analizar el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar el iframe del mapa
        iframes = soup.find_all('iframe')

        iframes = iframes

        print(f"Iframes encontrados {len(iframes)}")

        # muestra el enlace de cada mapa en la pagina
        maps_ids = [get_iframe_data(iframe_tag) for iframe_tag in iframes]
        return maps_ids

    else:
        print(f"Error al acceder a la página: {response.status_code}")

def get_urls(url):
    print(f"Buscando URLs {url}")
    # Configurar Firefox con WebDriver Manager
    service = Service(GeckoDriverManager().install())
    options = Options()
    options.add_argument("--headless")

    # Iniciar el navegador Firefox
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(url)  # Abrir la página

    # Esperar a que cargue la página (puedes ajustar este tiempo)
    driver.implicitly_wait(10)

    # Encontrar todos los elementos <a> en la página
    links = driver.find_elements(By.TAG_NAME, 'a')
    driver.quit()

    # Extraer los atributos href de los enlaces
    urls = [
        link.get_attribute('href') 
        for link in links if link.get_attribute('href')]
    
    filtered_urls = np.unique(
        [_url for _url in urls if _url.startswith(f'{url}/')]) 

    # Imprimir las URLs encontradas
    print(f"URLs encontradas: {len(filtered_urls)}")
    for i, link in enumerate(filtered_urls, 1):
        maps_ids = get_maps(link)
        print(maps_ids)

        # TODO:
        # Agregar resultado a DataFrame de pandas
        # Descargar kml de mapa
    

if __name__ == "__main__":
    for zone in zones:
        path = zone['path']
        url_zone = f"{main_url}/{path}"
        urls = get_urls(url_zone)