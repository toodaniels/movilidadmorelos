from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

# Configurar el navegador Firefox utilizando Geckodriver automático
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Abrir la página web
url = 'https://sites.google.com/view/movilidadmorelos/oriente/ruta-1-oriente'
driver.get(url)

# Esperar a que la página se renderice si es necesario
driver.implicitly_wait(10)  # Ajusta el tiempo según sea necesario

# Obtener el contenido renderizado
html = driver.page_source

# Parsear el HTML renderizado con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Buscar etiquetas <a> o cualquier elemento dinámico
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    if href:
        print(f"URL: {href}")

# Cerrar el navegador
driver.quit()

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Configurar el navegador Firefox utilizando Geckodriver automático
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Abrir la página web
driver.get("https://ejemplo.com")
print(driver.title)

# Cerrar el navegador
driver.quit()
