import csv
import time
from typing import List
from datetime import datetime
from config import config
import openpyxl
from descriptions import get_description
from get_from_xlsx_files import get_product_type_from_xlsx_file, get_make_model_generation_from_xlsx_file


def main():
    # Создание результирующего файла с заголовком
    init_csv_result_file()

    # запись в результирующий файл, возвращение ошибок
    errors_count, error_rows_numbers = write_result_file(config["filename_from_1c"])

    # запись ошибок в errors.txt
    write_error_rows(errors_count, error_rows_numbers)


def write_result_file(filename: str) -> (int, List[int]):
    """Получение данных из файла выгрузки из 1С, запись в результирующий файл, возвращение ошибок"""
    skip_row_count = 0
    skipped_rows = []

    with open(filename, newline="\n", encoding="cp1251") as file:
        reader = csv.reader(file.read().splitlines(), delimiter=';')
        count = 0

        for row in reader:
            # пропуск заголовка
            if count == 0:
                count += 1
                continue

            # debug version
            if count > 10:
                break

            print(f"Обрабатывается строка № {count}")

            # пропускаем неполные и пустые строки
            if len(row) < 34 or row[0] != "Товары":
                count += 1
                skip_row_count += 1
                skipped_rows.append(count)
                continue

            # получаем готовую строку для записи
            result_row = get_result_row(row)

            write_to_csv_file(result_row)

            count += 1

    return skip_row_count, skipped_rows


def get_result_row(csv_row: list) -> list:
    """Формирование финальной строки для авито из строки csv файла"""
    result_row = []

    result_row.append(csv_row[4])   # Id
    result_row.append("")   # AvitoId

    if config["version"] == "windows":
        result_row.append(config["manager_name"].encode("cp1251").decode("utf-8"))  # ManagerName
        result_row.append(config["contact_phone"].encode("cp1251").decode("utf-8"))  # ContactPhone
        result_row.append(config["address"].encode("cp1251").decode("utf-8"))  # Address
        result_row.append(config["category"].encode("cp1251").decode("utf-8"))  # Category
    else:
        result_row.append(config["manager_name"])  # ManagerName
        result_row.append(config["contact_phone"])  # ContactPhone
        result_row.append(config["address"])  # Address
        result_row.append(config["category"])  # Category

    result_row.append(csv_row[2])   # Title

    if config["version"] == "windows":
        result_row.append(config["goods_type"].encode("cp1251").decode("utf-8"))  # GoodsType
        result_row.append(config["ad_type"].encode("cp1251").decode("utf-8"))  # AdType
    else:
        result_row.append(config["goods_type"])  # GoodsType
        result_row.append(config["ad_type"])  # AdType

    product_info = get_product_types(csv_row[12], csv_row[13])
    result_row.append(product_info[0])  # ProductType
    result_row.append(product_info[1])  # SparePartType
    result_row.append(product_info[2])  # EngineSparePartType
    result_row.append(product_info[3])  # BodySparePartType
    result_row.append(product_info[4])  # DeviceType

    description = get_description(csv_row)
    result_row.append(description)  # Description

    result_row.append(csv_row[1])  # Condition

    if config["version"] == "windows":
        result_row.append(config["availability"].encode("cp1251").decode("utf-8"))  # Availability
    else:
        result_row.append(config["availability"])  # Availability

    result_row.append(csv_row[15])  # Brand
    result_row.append(csv_row[33])  # ImageUrls

    oem_filed = get_oem_field(csv_row)
    result_row.append(oem_filed)    # OEM

    # result_row.append("ПУСТАЯ СТРОКА")  # S пустая строка TODO убрать

    make_model_generation = get_make_model_generation(csv_row[15], csv_row[16], csv_row[17])
    result_row.append(make_model_generation[0])  # Make строка
    result_row.append(make_model_generation[1])  # Model строка
    result_row.append(make_model_generation[2])  # Generation строка
    result_row.append(make_model_generation[3])  # Modification строка
    result_row.append(make_model_generation[4])  # FuelType строка
    result_row.append(make_model_generation[5])  # DriveType строка
    result_row.append(make_model_generation[6])  # Transmission строка
    result_row.append(make_model_generation[7])  # BodyType строка
    result_row.append(make_model_generation[8])  # Doors строка

    if config["version"] == "windows":
        result_row.append(config["ad_status"])   # AdStatus
    else:
        result_row.append(config["ad_status"])  # AdStatus

    result_row.append(csv_row[14])   # Price

    return result_row


def get_product_types(group_M: str, sub_group_N: str) -> list:
    """Сопоставляем М (12), N (13) с G в таблице соответствия и полями B(1), C(2), D(3) заполняет поля J, K, L"""
    result = []
    for row in PRODUCT_TYPES:
        if row[5] == group_M and row[6] == sub_group_N:
            result.append(row[0])
            result.append(row[1])
            result.append(row[2])
            result.append(row[3])
            result.append(row[4])

    if not result:
        return ["ЗАГЛУШКА 1", "ЗАГЛУШКА 2", "ЗАГЛУШКА 3", "ЗАГЛУШКА 4", "ЗАГЛУШКА 5"]
    return result


# TODO разобраться с пробелами
def get_oem_field(row: list) -> str:
    """Получает ОЕМ из 1С колонка F or H or L или случайное число"""
    if row[5].replace(" ", ""):
        oem = row[5]
    elif row[7].replace(" ", ""):
        oem = row[7]
    elif row[3].replace(" ", ""):
        oem = row[3]
    else:
        global RANDOM_OEM
        oem = str(RANDOM_OEM)
        RANDOM_OEM += 1

    return oem


def get_make_model_generation(make: str, model: str, generation: str) -> list:
    """Получение Make Model Generation Modification FuelType DriveType Transmission
    BodyType Doors по P Q R из 1С файла"""
    for row in MAKES_MODELS_GENERATIONS:
        if row[10] == make and row[11] == model and row[12] == generation:
            return row

    return ["ЗАГЛУШКА 1", "ЗАГЛУШКА 2", "ЗАГЛУШКА 3", "ЗАГЛУШКА 4", "ЗАГЛУШКА 5", "ЗАГЛУШКА 6", "ЗАГЛУШКА 7", "ЗАГЛУШКА 8", "ЗАГЛУШКА 9"]


def write_to_csv_file(row: list):
    """Записывает результат в csv файл"""
    with open(config["filename_result"], 'a', newline="\n", encoding=config["result_encoding"]) as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(row)


def init_csv_result_file():
    """Создает файл для записи результатов и устанавливает заголовок"""
    header = ["Id", "AvitoId", "ManagerName", "ContactPhone", "Address", "Category",
              "Title", "GoodsType", "AdType", "ProductType", "SparePartType", "EngineSparePartType", "BodySparePartType",
              "DeviceType", "Description", "Condition", "Availability", "Brand", "ImageUrls", "OEM", "Make", "Model",
              "Generation", "Modification", "FuelType", "DriveType", "Transmission", "BodyType", "Doors", "AdStatus", "Price"]
    with open(config["filename_result"], 'w', newline="\n", encoding="cp1251") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(header)


def write_error_rows(skip_row_count: int, skipped_rows: List[int]):
    """Записывает необработанные строки из файла выгрузки 1С"""
    if skip_row_count > 0:
        text = f"Пропущено строк: {skip_row_count}\n\nНомера пропущенных строк в файле выгрузки из 1С:\n{' '.join([f'{row_number};' for row_number in skipped_rows])}"
        with open("errors.txt", "w") as file:
            file.write(text)
        print(f"Пропущено строк: {skip_row_count}. Их номера записаны в файле errors.txt")
    else:
        print("Все строки записаны, ошибок нет")


if __name__ == "__main__":
    PRODUCT_TYPES = get_product_type_from_xlsx_file()
    MAKES_MODELS_GENERATIONS = get_make_model_generation_from_xlsx_file()
    RANDOM_OEM = int(datetime.now().timestamp() * 1_000_000)

    start = datetime.now()
    main()
    end = datetime.now()
    print(end - start)