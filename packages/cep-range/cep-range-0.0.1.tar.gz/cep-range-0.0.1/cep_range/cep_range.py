from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import re


class InvalidCEPError(Exception):
    pass


class CoordinatesNotFoundError(Exception):
    pass


def validate_cep(cep):
    cep = ''.join(re.findall(r'\d+', str(cep)))
    if len(cep) != 8:
        raise InvalidCEPError('Erro: CEP inválido')
    else:
        return cep[:5] + '-' + cep[5:]


def get_coordinates(cep):
    try:
        # Configurar o modo headless
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        # Inicializar o navegador
        driver = webdriver.Chrome(options=options)

        # Abrir o link do Google Maps
        driver.get(f"https://www.google.com/maps/place/{cep}")

        # Aguardar a presença do elemento da barra de pesquisa
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchbox-searchbutton"))
        )

        # Clicar no botão de pesquisa
        search_button.click()

        # Aguardar o carregamento da página
        WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))

        # Obter a nova URL
        url = driver.current_url

        # Extrair as coordenadas da URL usando regex
        coord_regex = r"@(-?\d+\.\d+),(-?\d+\.\d+)"
        matches = re.search(coord_regex, url)

        # Verificar se houve correspondência e obter as coordenadas
        if matches:
            latitude = matches.group(1)
            longitude = matches.group(2)
            coordenadas = float(latitude), float(longitude)
            return coordenadas
        else:
            print("Coordenadas não encontradas na URL.")

    except Exception as e:
        print("Ocorreu um erro:", str(e))

    finally:
        # Fechar o navegador
        driver.quit()


def calculate_distance(cep_1, cep_2, unit):
    try:
        coord_1 = get_coordinates(validate_cep(cep_1))
        coord_2 = get_coordinates(validate_cep(cep_2))
        # Converter as coordenadas de graus para radianos
        lat1 = coord_1[0]
        lon1 = coord_1[1]
        lat2 = coord_2[0]
        lon2 = coord_2[1]

        if (lat1 == lat2) and (lon1 == lon2):
            return 0
        else:
            theta = lon1 - lon2
            dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(
                math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
            dist = math.acos(dist)
            dist = math.degrees(dist)
            miles = dist * 60 * 1.1515
            unit = unit.upper()

            if unit == 'KM':
                return "{:.3f}".format(miles * 1.609344)
            else:
                return "{:.3f}".format((miles * 1.609344) * 1000)

    except CoordinatesNotFoundError:
        raise ValueError('Erro: Coordenadas não encontradas')


def get_cep(latitude, longitude):
    geolocator = Nominatim(user_agent='my-app')
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)

    if location is not None and 'address' in location.raw:
        address = location.raw['address']
        if 'postcode' in address:
            return address['postcode']
    else:
        raise 'Erro: Não foi possível converter as coordenadas em CEP'


def ceps_range(raio_m, cep_c):

    coords = get_coordinates(validate_cep(cep_c))

    centro_lat = coords[0]
    centro_lon = coords[1]

    # Converter raio de metros para graus de latitude e longitude
    graus_lat = raio_m / 111000
    graus_lon = raio_m / (111000 * math.cos(math.radians(centro_lat)))

    # Calcular o número de pontos em uma linha
    pontos_por_linha = int(math.ceil((raio_m * 2) / 50))

    # Calcular o espaçamento entre os pontos
    espacamento_lat = graus_lat / (pontos_por_linha - 1)
    espacamento_lon = graus_lon / (pontos_por_linha - 1)

    coord = [(centro_lat + (i * espacamento_lat), centro_lon + (j * espacamento_lon))
             for i in range(pontos_por_linha) for j in range(pontos_por_linha)]

    ceps_unicos = set()
    for cd in coord:
        cep = get_cep(cd[0], cd[1])
        if cep is not None:
            ceps_unicos.add(cep)

    return list(ceps_unicos)

