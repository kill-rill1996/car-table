import csv
from typing import List
from datetime import datetime
from config import config
import openpyxl


def main():
    init_csv_result_file()
    open_1c_file(config["filename_from_1c"])


def open_1c_file(filename: str):
    with open(filename, newline="\n", encoding="cp1251") as file:
        reader = csv.reader(file.read().splitlines(), delimiter=';')
        count = 0
        skip_row_count = 0
        skipped_rows = []

        for row in reader:
            # пропуск заголовка
            if count == 0:
                count += 1
                continue

            if count > 1000:
                return

            print(f"Обрабатывается строка № {count}")

            if len(row) < 34 or row[0] != "Товары":
                count += 1
                skip_row_count += 1
                skipped_rows.append(count)
                continue

            result_row = get_result_row(row)

            write_to_csv_file(result_row)

            count += 1

        wirte_error_rows(skip_row_count, skipped_rows)


def get_result_row(csv_row: list) -> list:
    """Формирование финальной строки для авито из строки csv файла"""
    result_row = []

    result_row.append(csv_row[4])   # Id
    result_row.append("")   # AvitoId
    result_row.append(config["manager_name"])   # ManagerName
    result_row.append(config["contact_phone"])   # ContactPhone
    result_row.append(config["address"])   # Address
    result_row.append(config["category"])   # Category
    result_row.append(csv_row[2])   # Title
    result_row.append(config["goods_type"])  # GoodsType
    result_row.append(config["ad_type"])  # AdType

    product_info = get_product_types(csv_row[12], csv_row[13])
    result_row.append(product_info[0])  # ProductType
    result_row.append(product_info[1])  # SparePartType
    result_row.append(product_info[2])  # EngineSparePartType

    description = get_description(csv_row)
    result_row.append(description)  # Description

    result_row.append(csv_row[1])  # Condition
    result_row.append(config["availability"])  # Availability

    result_row.append(csv_row[15])  # Brand
    result_row.append(csv_row[33])  # ImageUrls

    oem_filed = get_OEM_field(csv_row)
    result_row.append(oem_filed)    # OEM

    result_row.append("ПУСТАЯ СТРОКА")  # S пустая строка TODO убрать
    result_row.append("Make")  # Make строка TODO
    result_row.append("Model")  # Model строка TODO
    result_row.append("Generation")  # Generation строка TODO

    result_row.append(config["ad_status"])   # AdStatus
    result_row.append(csv_row[14])   # Price

    return result_row


def get_product_types(group_M: str, sub_group_N: str) -> list:
    """Сопоставляем М (12), N (13) с G в таблице соответствия и полями B(1), C(2), D(3) заполняет поля J, K, L"""
    file = openpyxl.load_workbook("compare_table.xlsx")
    sheet_obj = file.active
    values_area = sheet_obj["B3":"H339"]
    result = []

    for row in values_area:
        row_values = []
        for cell in row:
            row_values.append(cell.value)

        if row_values[5] == group_M and row_values[6] == sub_group_N:
            result.append(row_values[0])
            result.append(row_values[1])
            result.append(row_values[2])

    if not result:
        return ["ЗАГЛУШКА 1", "ЗАГЛУШКА 2", "ЗАГЛУШКА 3"]
    return result


# TODO разобраться с пробелами
def get_OEM_field(row: list) -> str:
    """Получает ОЕМ из 1С колонка F or H or L"""
    if row[5].replace(" ", ""):
        oem = row[5]
    elif row[7].replace(" ", ""):
        oem = row[7]
    elif row[3].replace(" ", ""):
        oem = row[3]
    else:
        unique_value = datetime.now().timestamp()
        oem = unique_value
    # else:
    #     oem = row[11].replace(" ", "")
    if "E+" in oem:
        unique_value = datetime.now().timestamp()
        oem = unique_value

    return oem


# TODO
def get_description(row: list) -> str:
    """Заполняется по правилам для группы товара"""
    return "".join(row)


def write_to_csv_file(row: list):
    """Записывает результат в csv файл"""
    # прод версия
    # with open(config["filename_result"], 'a', newline="\n", encoding="cp1251") as file:

    # для отладки
    with open(config["filename_result"], 'a', newline="\n") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(row)


def init_csv_result_file():
    """Создает файл для записи результатов и устанавливает заголовок"""
    header = ["Id", "AvitoId", "ManagerName", "ContactPhone", "Address", "Category",
              "Title", "GoodsType", "AdType", "ProductType", "SparePartType", "EngineSparePartType",
              "Description", "Condition", "Availability", "Brand", "ImageUrls", "OEM", " ", "Make", "Model",
              "Generation", "AdStatus", "Price"]
    with open(config["filename_result"], 'w', newline="\n") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(header)


def wirte_error_rows(skip_row_count: int, skipped_rows: List[int]):
    """Записывает необработанные строки из файла выгрузки 1С"""
    text = f"Пропущено строк: {skip_row_count}\nНомера строк:\n{[f'{row_number};' for row_number in skipped_rows]}"
    with open("errors.txt", "w") as file:
        file.write(text)


if __name__ == "__main__":
    main()