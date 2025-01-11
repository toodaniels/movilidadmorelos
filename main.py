import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager


main_url = "https://sites.google.com/view/movilidadmorelos"

zones = [
    { 'id': 'CENTRO', 'name': 'Centro', 'path': 'centro' },
    # { 'id': 'SUR', 'name': 'Sur', 'path': 'sur' },
    # { 'id': 'ORIENTE', 'name': 'Oriente', 'path': 'oriente' },
    # { 'id': 'RUTA_DE_LA_SALUD', 'name': 'Ruta de salud', 'path': 'ruta-de-la-salud' }
]

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

    # Extraer los atributos href de los enlaces
    urls = [
        link.get_attribute('href') 
        for link in links if link.get_attribute('href')]
    print(urls)
    # Filtrar usando filter
    filtered_urls = filter(lambda _url: _url.startswith(f'{url}/'), urls)

    # Convertir el resultado a lista si lo necesitas
    filtered_urls = list(filtered_urls)

    # Imprimir las URLs encontradas
    print("URLs encontradas:")
    for i, link in enumerate(filtered_urls, 1):
        print(f"{i}: {link}")

    # Cerrar el navegador
    driver.quit()


def get_map(url):
    # Hacer la solicitud
    response = requests.get(url)
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
            map_id =  src.replace(
                'https://www.google.com/maps/d/embed?mid=', '')
            print(f"Mapa ID: {map_id}")
            print(route_code, route_title)
    else:
        print(f"Error al acceder a la página: {response.status_code}")


if __name__ == "__main__":
    for zone in zones:
        path = zone['path']
        url_zone = f"{main_url}/{path}"
        get_urls(url_zone)