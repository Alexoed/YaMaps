import sys
from io import BytesIO

import requests
from PIL import Image


class ImageGenerator:
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    map_api_server = "http://static-maps.yandex.ru/1.x/"

    def __init__(self):
        file = open("key.txt", mode="rt")
        self.api_key = file.read().strip()
        file.close()

    def get_from_toponym(self, address: str, delta):
        geocoder_params = {
            "apikey": self.api_key,
            "geocode": address,
            "format": "json"}

        response = requests.get(self.geocoder_api_server,
                                params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            pass

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        top_longitude, top_lattitude = toponym_coodrinates.split(" ")

        return self.get_from_cords(top_longitude, top_lattitude, delta)

    def get_from_cords(self, longitude, lattitude, delta):
        map_params = {
            "ll": ",".join([longitude, lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }

        response = requests.get(self.map_api_server, params=map_params)
        # Запишем полученное изображение в файл.
        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        return response.content, map_file


def main():
    ig = ImageGenerator()
    Image.open(BytesIO(ig.get_from_toponym("Кириши, ленинградская 6",
                                           "0.0002")[0])).show()


if __name__ == "__main__":
    main()
