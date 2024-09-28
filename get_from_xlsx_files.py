import openpyxl


def get_make_model_generation_from_xlsx_file() -> list:
    """Получение всех Make Model Generation Modification FuelType DriveType Transmission
    BodyType Doors из второй сравнительной таблицы"""
    file = openpyxl.load_workbook("compare_table_cars.xlsx")
    sheet_obj = file.active
    values_area = sheet_obj["A2":"M21370"]
    result = []

    for row in values_area:
        result_row = []
        if row[10]:
            for cell in row:
                result_row.append(cell.value)
            result.append(result_row)

    return result


def get_product_type_from_xlsx_file() -> list:
    """Получение всех ProductType из первой сравнительной таблицы"""
    file = openpyxl.load_workbook("compare_table_groups.xlsx")
    sheet_obj = file.active
    values_area = sheet_obj["B3":"H339"]
    result = []

    for row in values_area:
        result_row = []
        for cell in row:
            result_row.append(cell.value)
        result.append(result_row)

    return result

