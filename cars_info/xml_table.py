import csv
from typing import List

import requests
import xml.etree.ElementTree as ET


URL = "http://autoload.avito.ru/format/Autocatalog.xml"
RESULT_CSV_FILE_NAME = "all_cars.csv"


def main():
    download_xml_cars_file()
    result_rows = get_all_cars_info()
    write_csv_file(result_rows)


def download_xml_cars_file():
    """Скачиваем XML файл"""
    print("Скачивание XML файла....")
    response = requests.get(URL)
    with open('cars.xml', 'wb') as file:
        file.write(response.content)


def get_all_cars_info() -> List[List]:
    """Получаем информацию обо всех машинах из XML файла"""
    print("Получение данных из XML файла...")
    root = ET.parse('cars.xml').getroot()

    result_rows = []

    for make in root.findall('Make'):
        make_name = make.get("name")

        for model in make.findall("Model"):
            model_name = model.get("name")

            for generation in model.findall("Generation"):
                generation_name = generation.get("name")

                for modification in generation.findall("Modification"):
                    modification_name = modification.get("name")
                    fuel_type = modification.find("FuelType").text
                    drive_type = modification.find("DriveType").text
                    transmission = modification.find("Transmission").text
                    body_type = modification.find("BodyType").text
                    doors = modification.find("Doors").text
                    result_rows.append([make_name, model_name, generation_name, modification_name, fuel_type, drive_type,
                                        transmission, body_type, doors])

    return result_rows


def write_csv_file(rows: List[List]):
    """Запись результата в CSV файл"""
    print("Запись в CSV файл...")
    header = ["Make id", "Model id", "Generation id", "Modification id", "FuelType id",	"DriveType id", "Transmission id",
              "BodyType id", "Doors id"]

    # write header
    with open(RESULT_CSV_FILE_NAME, 'w', newline="\n") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(header)

    for row in rows:
        with open(RESULT_CSV_FILE_NAME, 'a', newline="\n") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(row)


if __name__ == "__main__":
    main()


