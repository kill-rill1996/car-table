import csv
import os
from typing import List

import xml.etree.ElementTree as ET

BASEDIR = os.path.dirname(os.path.abspath(__file__))
XML_FILE_NAME = os.path.join(BASEDIR, "truck.xml")
RESULT_CSV_FILE_NAME = os.path.join(BASEDIR, "trucks.csv")


def main():
    result_rows = get_all_cars_info()
    write_csv_file(result_rows)


def get_all_cars_info() -> List[List]:
    """Получаем информацию обо всех машинах из XML файла"""
    print("Получение данных из XML файла...")
    root = ET.parse(XML_FILE_NAME).getroot()

    result_rows = []

    for make in root.findall("Make"):
        for model in make.findall("Model"):
            for body_type in model.findall("BodyType"):
                for wheel_formula in body_type.findall("WheelFormula"):
                    for engine_type in wheel_formula.findall("EngineType"):
                        for power in engine_type.findall("Power"):
                            for transmission in power.findall("Transmission"):
                                make_name = str(make.get("name"))
                                model_name = str(model.get("name"))
                                body_type_name = str(body_type.get("name"))
                                wheel_formula_name = str(wheel_formula.get("name"))
                                engine_type_name = str(engine_type.get("name"))
                                power_name = str(power.get("name"))
                                transmission_name = str(transmission.get("name"))

                                result_rows.append([make_name, model_name, body_type_name, wheel_formula_name,
                                                    engine_type_name, power_name, transmission_name])

    return result_rows


def write_csv_file(rows: List[List]):
    """Запись результата в CSV файл"""
    print("Запись в CSV файл...")
    header = ["Make", "Model", "BodyType", "WheelFormula", "EngineType", "Power", "Transmission"]

    # write header
    with open(RESULT_CSV_FILE_NAME, 'w', newline="\n", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(header)

    # write rows
    with open(RESULT_CSV_FILE_NAME, 'a', newline="\n", encoding="utf-8") as file:
        for row in rows:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(row)


if __name__ == "__main__":
    main()


