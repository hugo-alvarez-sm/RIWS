import scrapy
from bs4 import BeautifulSoup
import json

class AlbumsSpider(scrapy.Spider):
    name = "albums"
    allowed_domains = ["albumoftheyear.org"]
    start_urls = ["https://albumoftheyear.org/artist/719-drake/"]

    def parse(self, response):
        # Parsear el contenido de la página con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra y procesa los elementos <div> con la clase "albumBlock"
        divs_album = soup.find_all('div', class_="albumBlock small")

        for div_album in divs_album:
            # Comprueba si el elemento <div> tiene un atributo data-type válido
            data_type = div_album.get('data-type')

            if data_type in ["lp", "mixtape", "ep"]:
                # Encuentra el elemento <a> dentro del elemento <div>
                a_element = div_album.find('a', href=True)

                if a_element:
                    # Obtiene la URL
                    album_url = a_element['href']
                    print("URL del álbum:", album_url)

                    # Realiza una nueva solicitud web para la URL del álbum y pasa la URL a la función de devolución de llamada "self.parse_album"
                    yield response.follow(album_url, callback=self.parse_album)

    def parse_album(self, response):
        # Analiza el contenido HTML de la página del álbum
        # Aquí puedes extraer información adicional, como el título del álbum, críticas, etc.
        soup = BeautifulSoup(response.text, 'html.parser')

        # Obtener datos principales 
        album_artist = soup.find('div', class_="artist").get_text()
        print(album_artist)
        album_title = soup.find('div', class_="albumTitle").get_text()
        print(album_title)
        album_rating = soup.find('a', href ="#critics").get_text()
        based_on = soup.find('div', class_="text numReviews").get_text()
        print("Score: ",album_rating," ",based_on)


        #Obtener metadatos (Sin Terminar)
        album_info_box = soup.find('div', class_="detailRow")
        info = album_info_box.find_all('a')
        print(info)
        # Inicializa una lista para almacenar los textos de los elementos <a>
        date_list = []

        # Itera a través de los elementos <a> y almacena sus textos en la lista
        for element in info:
            date_item = element.get_text(strip=True)
            date_list.append(date_item)

        # Convierte la lista de textos en una cadena, separados por comas
        date_string = ', '.join(date_list)

        print(date_string)


        # Encuentra el elemento con la clase "trackListTable"
        track_list_table = soup.find('table', class_="trackListTable")

        if track_list_table:
            # Inicializa una lista para almacenar las canciones
            songs = []

            # Encuentra todas las filas <tr> dentro de la tabla
            rows = track_list_table.find_all('tr')

            for row in rows:
                # Encuentra las celdas <td> que contienen el número de pista, título y duración
                cells = row.find_all('td')

                if len(cells) >= 3:
                    track_number = cells[0].get_text(strip=True)
                    track_title = cells[1].find('a').get_text(strip=True)
                    track_duration = cells[1].find('div', class_="length").get_text(strip=True)
                    
                    # Almacena la información de la canción en un diccionario
                    song_info = {
                        "Número de pista": track_number,
                        "Título de la canción": track_title,
                        "Duración": track_duration
                    }
                    songs.append(song_info)

            # Calcula la duración total
            total_length = soup.find('div', class_="totalLength").get_text(strip=True)

            print("Canciones:")
            for song in songs:
                print(song)

            print("Duración total:", total_length)


            # Ejecutar spider con el comando "scrapy crawl albums"


    





    



