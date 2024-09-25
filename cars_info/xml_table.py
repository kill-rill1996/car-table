import csv
import os
from typing import List

import requests
import xml.etree.ElementTree as ET

BASEDIR = os.path.dirname(os.path.abspath(__file__))
XML_FILE_URL = "http://autoload.avito.ru/format/Autocatalog.xml"
XML_FILE_NAME = os.path.join(BASEDIR, "cars.xml")
RESULT_CSV_FILE_NAME = os.path.join(BASEDIR, "cars.csv")


def main():
    download_xml_cars_file()
    result_rows = get_all_cars_info()
    write_csv_file(result_rows)
    os.remove(XML_FILE_NAME)


def download_xml_cars_file():
    """Скачиваем XML файл"""
    print("Скачивание XML файла....")
    response = requests.get(XML_FILE_URL)
    with open(XML_FILE_NAME, 'wb') as file:
        file.write(response.content)


def get_all_cars_info() -> List[List]:
    """Получаем информацию обо всех машинах из XML файла"""
    print("Получение данных из XML файла...")
    root = ET.parse(XML_FILE_NAME).getroot()

    result_rows = []

    for make in root.findall('Make'):
        # make_name = make.get("name")

        for model in make.findall("Model"):
            # model_name = model.get("name")

            for generation in model.findall("Generation"):
                # generation_name = generation.get("name")

                for modification in generation.findall("Modification"):
                    make_name = modification.find("Make").text
                    model_name = modification.find("Model").text
                    generation_name = modification.find("Generation").text
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
    header = ["Make", "Model", "Generation", "Modification", "FuelType", "DriveType", "Transmission", "BodyType", "Doors"]

    # write header
    with open(RESULT_CSV_FILE_NAME, 'w', newline="\n", encoding="cp1251") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(header)

    # write rows
    for row in rows:
        with open(RESULT_CSV_FILE_NAME, 'a', newline="\n", encoding="cp1251") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(row)


if __name__ == "__main__":
    main()


