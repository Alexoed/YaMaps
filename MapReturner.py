import sys
from io import BytesIO
from pprint import pprint
import requests
from PIL import Image


class ImageGenerator:
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    map_api_server = "http://static-maps.yandex.ru/1.x/"

    def __init__(self):
        self.address = "пока ничего не искалось"
        self.postal_code = ""
        self.add_postal_code = False
        file = open("key.txt", mode="rt")
        self.api_key = file.read().strip()
        file.close()
        self.pos = (0, 0)
        self.layer = "map"
        self.point = "0,0"

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
        try:
            self.postal_code = json_response["response"][
                "GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                "metaDataProperty"]["GeocoderMetaData"][
                "Address"]["postal_code"]
        except Exception as ex:
            print(type(ex), ex)
            self.postal_code = ""
        try:
            self.address = json_response["response"][
                "GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                "metaDataProperty"]["GeocoderMetaData"][
                "Address"]["formatted"]
        except Exception as ex:
            print(type(ex), ex)
            self.address = "Увы, не нашлось"
        try:
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
        except IndexError as ie:
            return print(f"Ошибка: не удалось найти {ie}")
        except KeyError as ke:
            return print(f"Ошибка: не удалось найти {ke}")
        self.pos = toponym_coodrinates.split(" ")
        self.point = "{0},{1}".format(*self.pos)

        return self.get_from_cords(*self.pos, delta)

    def get_from_cords(self, longitude, lattitude, delta):
        map_params = {
            "ll": ",".join([longitude, lattitude]),
            "spn": ",".join([delta, delta]),
            "l": self.layer,
            "pt": "{0},pm2dgl".format(self.point)
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

    def get_position(self):
        return self.pos

    def set_layer(self, layer="map"):
        self.layer = layer

    def get_address(self):
        if self.add_postal_code:
            return self.address + ", почтовый " \
                                  "индекс: " + self.postal_code
        return self.address

    def set_postalcode(self, value: bool):
        self.add_postal_code = value


def main():
    ig = ImageGenerator()
    Image.open(BytesIO(ig.get_from_toponym("Кириши, ленинградская 6",
                                           "0.0002")[0])).show()


if __name__ == "__main__":
    main()
