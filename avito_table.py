import csv
import io
import math
from datetime import datetime
from functools import wraps
from typing import Callable
from xml.etree import ElementTree as ET

from config import get_config
from descriptions import get_description, get_description_drom
from get_from_xlsx_files import get_product_type_from_xlsx_file, get_make_model_generation_from_xlsx_file


def process_time(func: Callable):
    """Измерение времени выполнения программы"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()

        func(*args, **kwargs)

        end = datetime.now()
        work_time = end - start
        print(f"\nВремя выполнения программы {work_time}")

    return wrapper


class AvitoTable:

    def __init__(self):
        self.row_count: int = 0
        self.errors: dict[int:list] = {}
        self.config: dict = get_config()
        self.skip_rows_count: int = 0
        self.PRODUCT_TYPES = get_product_type_from_xlsx_file(self.config["compare_table_groups"])
        self.MAKES_MODELS_GENERATIONS: list[list] = get_make_model_generation_from_xlsx_file(self.config["compare_table_cars"])
        self.RANDOM_OEM = 10000210011

    @process_time
    def make_avito_table(self):
        """Создает готовый файл csv с требованиями Avito"""
        # инициализирует файл
        print("\nИнициализация csv файла...")

        if self.config["need_upload_file"]:
            # файл для отправки
            self.init_csv_result_file(to_upload=True)

        if self.config["need_xml_file"]:
            self.init_xml_file()

        # файл для чтения
        self.init_csv_result_file()

        # запись в файл для дрома
        if self.config["need_drom_file"]:
            self.init_drom_result_file()

        # записывает в файл готовые строки
        print("\nЗапись строк в файл...")
        self.write_result_csv_file()

        # записывает список ошибок
        print("\nФормирование файла ошибок...")
        self.write_error_rows()

    def _generator(self, file):
        with open(file, newline="\n", encoding=self.config["1C_file_encoding"]) as f:
            reader = csv.reader(f.read().splitlines(), delimiter=';')
            for row in reader:
                yield row

    def write_result_csv_file(self):
        """Получение данных из файла выгрузки из 1С, запись в результирующий файл, возвращение ошибок"""

        generator = self._generator(self.config["filename_from_1c"])

        for row in generator:
            # пропуск заголовка
            if self.row_count == 0:
                self.row_count += 1
                continue

            # запись xml файла
            if self.config["need_xml_file"]:
                self.write_xml_file(row)

            # debug version
            if self.config["max_rows"] != -1:
                if self.row_count > self.config["max_rows"]:
                    break

            print(f"Обрабатывается строка № {self.row_count}")

            # пропускаем неполные и пустые строки
            if not self._is_row_valid(row):
                continue

            self.row_count += 1

            # получаем готовую строку для записи в авито таблицу
            result_row = self._get_result_row(row)

            # запись для чтения
            self.write_to_csv_file(result_row)

            if self.config["need_upload_file"]:
                # запись для отправки
                self.write_to_csv_file(result_row, to_upload=True)

            # запись в файл Дром с подготовкой строки с изменениями
            if self.config["need_drom_file"]:
                add_params = {
                    "L-R": row[25],
                    "U-D": row[26],
                    "F-R": row[27],
                    "count": row[32],
                    "units_of_meas": row[8],
                    "engine": row[21],
                    "detail_number": row[7],
                    "price": self._get_price(row[14], "commission_drom")
                }
                correct_row = self._create_correct_row_for_drom(result_row, add_params)
                self.write_to_drom_file(correct_row)


    def _is_row_valid(self, row: list) -> bool:
        """Проверяет валидность строки по длине и первому значению"""
        if len(row) < 34 or row[0] != "Товары":
            self.row_count += 1
            self.skip_rows_count += 1
            self._add_error("Некорректная строка")
            return False
        return True

    def _add_error(self, err_msg: str):
        """Записывает ошибку по строке"""
        if self.errors.get(self.row_count):
            self.errors[self.row_count].append(err_msg)
        else:
            self.errors[self.row_count] = [err_msg]

    def _get_result_row(self, csv_row: list) -> (list, list):
        """Формирование финальной строки для из строки csv файла
        result_row: [Id, AvitoId, ManagerName, ContactPhone, Address, Category, Title, GoodsType
        AdType, ProductType, SparePartType, EngineSparePartType, BodySparePartType, DeviceType
        Description, Condition, Availability, Brand, ImageUrls, OEM, Make, Model, Generation
        AdStatus, Price, TransmissionSparePartType]"""
        result_row = list()

        result_row.append(csv_row[4])  # Id
        result_row.append("")  # AvitoId

        if self.config["version"] == "windows":
            result_row.append(self.config["manager_name"].encode("cp1251").decode("utf-8"))  # ManagerName
            result_row.append(self.config["contact_phone"].encode("cp1251").decode("utf-8"))  # ContactPhone
            result_row.append(self.config["address"].encode("cp1251").decode("utf-8"))  # Address
            result_row.append(self.config["category"].encode("cp1251").decode("utf-8"))  # Category
        else:
            result_row.append(self.config["manager_name"])  # ManagerName
            result_row.append(self.config["contact_phone"])  # ContactPhone
            result_row.append(self.config["address"])  # Address
            result_row.append(self.config["category"])  # Category

        result_row.append(csv_row[2])  # Title

        if self.config["version"] == "windows":
            result_row.append(self.config["goods_type"].encode("cp1251").decode("utf-8"))  # GoodsType
            result_row.append(self.config["ad_type"].encode("cp1251").decode("utf-8"))  # AdType
        else:
            result_row.append(self.config["goods_type"])  # GoodsType
            result_row.append(self.config["ad_type"])  # AdType

        product_info = self._get_product_types(csv_row[12], csv_row[13])
        result_row.append(product_info[0])  # ProductType
        result_row.append(product_info[1])  # SparePartType
        result_row.append(product_info[2])  # EngineSparePartType
        result_row.append(product_info[3])  # BodySparePartType
        result_row.append(product_info[4])  # DeviceType

        # заранее получаем make model generation
        make_model_generation = self._get_make_model_generation(csv_row[15], csv_row[16], csv_row[17])

        description = get_description(csv_row, make_model_generation)
        result_row.append(description)  # Description

        result_row.append(csv_row[1])  # Condition

        if self.config["version"] == "windows":
            result_row.append(self.config["availability"].encode("cp1251").decode("utf-8"))  # Availability
        else:
            result_row.append(self.config["availability"])  # Availability

        result_row.append(csv_row[15])  # Brand
        result_row.append(csv_row[33])  # ImageUrls

        oem_filed = self._get_oem_field(csv_row)
        result_row.append(oem_filed)  # OEM

        # для грузовиков make model modification берем из исходника
        if csv_row[12] == "ГРУЗОВИК":
            result_row.append(csv_row[15])  # Make строка
            result_row.append(csv_row[16])  # Model строка
            result_row.append(csv_row[17])  # Generation строка
        # для всех остальных
        else:
            result_row.append(make_model_generation[0])  # Make строка
            result_row.append(make_model_generation[1])  # Model строка
            result_row.append(make_model_generation[2])  # Generation строка
            # result_row.append(make_model_generation[3])  # Modification строка
            # result_row.append(make_model_generation[4])  # FuelType строка
            # result_row.append(make_model_generation[5])  # DriveType строка
            # result_row.append(make_model_generation[6])  # Transmission строка
            # result_row.append(make_model_generation[7])  # BodyType строка
            # result_row.append(make_model_generation[8])  # Doors строка

        if self.config["version"] == "windows":
            result_row.append(self.config["ad_status"])  # AdStatus
        else:
            result_row.append(self.config["ad_status"])  # AdStatus

        rounded_price = self._get_price(csv_row[14], "commission_avito")
        result_row.append(rounded_price)  # Price

        result_row.append(product_info[5])  # TransmissionSparePartType
        result_row.append(product_info[6])  # TechnicSparePartType

        result_row.append(csv_row[22])  # Color

        if not self._check_correct_brand(csv_row):
            result_row[17] = result_row[20]

        return result_row

    def _get_product_types(self, group_m: str, sub_group_n: str) -> list:
        """Сопоставляем М (12), N (13) с G в таблице соответствия и полями B(1), C(2), D(3) заполняет поля J, K, L"""
        result = []
        for row in self.PRODUCT_TYPES:
            if row[6] == group_m and row[7] == sub_group_n:
                result.append(row[0])
                result.append(row[1])
                result.append(row[2])
                result.append(row[3])
                result.append(row[4])
                result.append(row[5])
                result.append(row[9])

                return result

        self._add_error(f"Не удалось найти соответствие ProductType, SparePartType, EngineSparePartType, "
                        f"BodySparePartType, DeviceType, TransmissionSparePartType по группе '{group_m}' "
                        f"и подгруппе '{sub_group_n}'")

        return ["", "", "", "", "", "", ""]

    def _get_oem_field(self, row: list) -> str:
        """Получает ОЕМ из 1С колонка F or H or L или случайное число"""
        if row[5].replace(" ", ""):
            oem = row[5]
        elif row[7].replace(" ", ""):
            oem = row[7]
        elif row[3].replace(" ", ""):
            oem = row[3]
        else:
            oem = str(self.RANDOM_OEM)
            self.RANDOM_OEM += 1
        return oem

    def _get_make_model_generation(self, make: str, model: str, modification: str) -> list:
        """Получение Make Model Generation Modification FuelType DriveType Transmission
        BodyType Doors по P Q R из 1С файла"""

        for row in self.MAKES_MODELS_GENERATIONS:
            if str(row[10]) == str(make) and str(row[11]) == str(model) \
                    and str(row[12]) == str(modification):
                return row

        self._add_error(f"Не удалось найти соответствие Make, Model, Generation по марке '{make}', модели '{model}' и модификации '{modification}'")
        return ["", "", ""]

    @staticmethod
    def _check_correct_brand(csv_row: list) -> bool:
        """Меняет поле Brand в результирующей таблице, если в таблице 1C поле марка(P)=ALL и поле B=Б/у"""
        if csv_row[1] == "Б/у" and csv_row[15] == "ALL":
            return False
        return True

    def write_to_csv_file(self, row: list, to_upload: bool = False):
        """Записывает результат в csv файл"""
        if to_upload:
            result_encoding = self.config["result_encoding_upload"]
            filename = self.config["result_encoding_upload_filename"]
        else:
            result_encoding = self.config["result_encoding_local"]
            filename = self.config["result_encoding_local_filename"]

        with open(filename, 'a', newline="\n", encoding=result_encoding) as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(row)

    def write_to_drom_file(self, row: list):
        """Записывает результирующую строку в файл для Дром"""
        filename = self.config["result_encoding_drom_filename"]
        result_encoding = self.config["result_encoding_drom"]

        with open(filename, 'a', newline="\n", encoding=result_encoding) as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(row)

    def write_xml_file(self, row: list):
        """Записывает данные в xml файл"""
        tree = ET.parse(self.config["xml_filename"])
        root = tree.getroot()

        offer_item = ET.SubElement(root, "offer")

        # code
        code_item = ET.SubElement(offer_item, "code")
        code_item.text = row[4]

        # title
        title_item = ET.SubElement(offer_item, "title")
        title_item.text = row[2]

        # is_new
        is_new_item = ET.SubElement(offer_item, "is_new")
        is_new_item.text = row[1]

        # brand
        brand_item = ET.SubElement(offer_item, "brand")
        brand_item.text = row[15]

        # model
        model_item = ET.SubElement(offer_item, "model")
        model_item.text = row[16]

        # modification
        modification_item = ET.SubElement(offer_item, "modification")
        modification_item.text = row[17]

        # category
        category_item = ET.SubElement(offer_item, "category")
        category_item.text = row[12]

        # sub_category
        sub_category_item = ET.SubElement(offer_item, "sub_category")
        sub_category_item.text = row[13]

        # spare_brand TODO (нет в таблице)
        # sub_category_item = ET.SubElement(offer_item, "sub_category")
        # sub_category_item.text = row[13]

        # country TODO (нет в таблице)
        # country_item = ET.SubElement(offer_item, "country")
        # country_item.text = row[13]

        # sku TODO (нет в таблице)
        # sku_item = ET.SubElement(offer_item, "sku")
        # sku_item.text = row[13]

        # spare_oem TODO (нет в таблице)
        # spare_oem_item = ET.SubElement(offer_item, "spare_oem")
        # spare_oem_item.text = row[5]

        # front_back TODO (нет в таблице)
        # front_back_item = ET.SubElement(offer_item, "front_back")
        # front_back_item.text = row[5]

        # top_bottom TODO (нет в таблице)
        # top_bottom_item = ET.SubElement(offer_item, "top_bottom")
        # top_bottom_item.text = row[5]

        # color TODO (нет в таблице)
        # color_item = ET.SubElement(offer_item, "color")
        # color_item.text = row[5]

        # comment TODO (нет в таблице)
        # comment_item = ET.SubElement(offer_item, "comment")
        # comment_item.text = row[5]

        # price
        price_item = ET.SubElement(offer_item, "price")
        price_item.text = row[14]

        # quantity TODO (нет в таблице)
        # quantity_item = ET.SubElement(offer_item, "quantity")
        # quantity_item.text = row[14]

        # gearbox_number TODO (нет в таблице)
        # gearbox_number_item = ET.SubElement(offer_item, "gearbox_number")
        # gearbox_number_item.text = row[14]

        # gearbox_number_alternative TODO (нет в таблице)
        # gearbox_number_alternative_item = ET.SubElement(offer_item, "gearbox_number_alternative")
        # gearbox_number_alternative_item.text = row[14]

        # oem TODO (уже есть spare_oem)
        oem_item = ET.SubElement(offer_item, "oem")
        oem_item.text = row[5].strip()

        # model_tovar TODO (нет в таблице)
        # model_tovar_item = ET.SubElement(offer_item, "model_tovar")
        # model_tovar_item.text = row[5]

        # images
        images_item = ET.SubElement(offer_item, "images")
        images_item.text = row[32]

        # images
        images_item = ET.SubElement(offer_item, "images")
        images_item.text = row[32]

        # сохраняем файл
        tree.write(self.config["xml_filename"], encoding=self.config["xml_file_encoding"], xml_declaration=True)

    def _create_correct_row_for_drom(self, avito_row: list, add_params: dict) -> list:
        """изменение строки для записи в авито в строку для записи в дром
        avito_row: [Id-0, AvitoId-1, ManagerName-2, ContactPhone-3, Address-4, Category-5, Title-6, GoodsType-7
        AdType-8, ProductType-9, SparePartType-10, EngineSparePartType-11, BodySparePartType-12, DeviceType-13
        Description-14, Condition-15, Availability-16, Brand-17, ImageUrls-18, OEM-19, Make-20, Model-21, Generation-22
        AdStatus-23, Price-24, TransmissionSparePartType-25]"""

        new_row = []

        new_row.append(avito_row[0])    # Артикул
        new_row.append(avito_row[6] + "_" + avito_row[0])    # Наименование товара
        new_row.append(avito_row[15])   # Новый/б.у.
        new_row.append(avito_row[20])   # Марка
        new_row.append(avito_row[21])   # Модель
        new_row.append(avito_row[22])   # Кузов
        new_row.append(avito_row[19])   # Номер
        new_row.append(add_params["engine"])   # Двигатель TODO
        new_row.append("")   # ГОД TODO

        if add_params["L-R"] != "":
            new_row.append(add_params["L-R"])   # L-R TODO
        else:
            new_row.append("")  # L-R TODO

        if add_params["F-R"] != "":
            new_row.append(add_params["F-R"])  # F-R TODO
        else:
            new_row.append("")  # F-R TODO

        if add_params["U-D"] != "":
            new_row.append(add_params["U-D"])  # U-D TODO
        else:
            new_row.append("")  # U-D TODO

        new_row.append("")  # Цвет TODO
        new_row.append(get_description_drom(avito_row[14]))  # Примечание

        new_row.append(add_params["count"])  # Количество TODO решили убрать пока

        new_row.append(add_params["price"])   # Цена с комиссией для дрома
        new_row.append(avito_row[16])   # Наличие
        new_row.append(add_params["detail_number"])  # номер детали TODO
        new_row.append(add_params["units_of_meas"])    # ед. изм TODO
        new_row.append(avito_row[18])   # фотографии
        return new_row

    def init_csv_result_file(self, to_upload: bool = False):
        """Создает файл для записи результатов и устанавливает заголовок"""
        header = ["Id", "AvitoId", "ManagerName", "ContactPhone", "Address", "Category",
                  "Title", "GoodsType", "AdType", "ProductType", "SparePartType", "EngineSparePartType",
                  "BodySparePartType", "DeviceType", "Description", "Condition", "Availability", "Brand", "ImageUrls",
                  "OEM", "Make", "Model", "Generation", "AdStatus", "Price", "TransmissionSparePartType",
                  "TechnicSparePartType", "Color"]

        if to_upload:
            result_encoding = self.config["result_encoding_upload"]
            filename = self.config["result_encoding_upload_filename"]

        else:
            result_encoding = self.config["result_encoding_local"]
            filename = self.config["result_encoding_local_filename"]

        with open(filename, 'w', newline="\n", encoding=result_encoding) as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)

    def init_drom_result_file(self):
        header = ["Артикул", "Наименование товара", "Новый/б.у.", "Марка", "Модель", "Кузов", "Номер",
                  "Двигатель", "Год", "L-R", "F-R", "U-D", "Цвет", "Примечание", "Количество", "Цена",
                  "Наличие", "№ Детали", "Ед.изм", "Фотографии"]
        result_encoding = self.config["result_encoding_drom"]

        with open(self.config['result_encoding_drom_filename'], "w", newline="\n", encoding=result_encoding) as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(header)

    def init_xml_file(self):
        root = ET.Element("offers")
        etree = ET.ElementTree(root)
        file = open(f"{self.config['xml_filename']}", "wb")
        etree.write(file, self.config["xml_file_encoding"], xml_declaration=True)

    def write_error_rows(self):
        """Записывает необработанные строки из файла выгрузки 1С в текстовый файл"""
        with open("errors.txt", "w") as file:
            file.write("СПИСОК ОШИБОК\n\n")

        if self.errors:
            header = f"Пропущено строк: {self.skip_rows_count}, всего ошибок: {len(self.errors)}\n\n" \
                   f"Ошибки в строках по номерам в файле выгрузки из 1С:\n\n"
            with open("errors.txt", "a") as file:
                file.write(header)

            for row_number, errors in self.errors.items():
                text = f"{row_number}. {' | '.join(errors)}\n"
                with open("errors.txt", "a") as file:
                    file.write(text)

            print(f"Пропущено строк: {self.skip_rows_count}, всего ошибок {len(self.errors)}, они записаны в файле errors.txt")
        else:
            with open("errors.txt", "a") as file:
                file.write("Все строки записаны, ошибок нет")
            print("Все строки записаны, ошибок нет")

    def _get_price(self, price: int | str, commission: str) -> int | None:
        """Получение цены"""
        try:
            int_price = int(price)
        except ValueError:

            try:
                int_price = int(price.split(",")[0])
            except ValueError:
                self._add_error(f"Некорректная цена: \"{price}\"")
                return
            return self._get_round_price_with_commission(int_price, commission)

        return self._get_round_price_with_commission(int_price, commission)

    @staticmethod
    def round_to_up(number: int) -> int:
        """Округляет вверх до ста"""
        return int(math.ceil(number / 100.0)) * 100

    @staticmethod
    def round_to_down(number: int) -> int:
        """Округляет всегда вверх до ста"""
        return int(math.floor(number / 100.0)) * 100

    @staticmethod
    def round_to_100(number: int) -> int:
        """Округляет число до 100"""
        if number <= 100:
            return 100
        if number % 100 > 50:
            return AvitoTable.round_to_up(number)
        else:
            return AvitoTable.round_to_down(number)

    def _get_round_price_with_commission(self, number: int, commission: str) -> int:
        """Округляет число до 100"""
        price_with_commission = number * (1 + self.config[f"{commission}"] / 100)
        return AvitoTable.round_to_100(price_with_commission)
