from datetime import datetime

from avito_table import AvitoTable


if __name__ == "__main__":
    start = datetime.now()

    avito_table = AvitoTable()
    avito_table.make_avito_table()

    end = datetime.now()
    work_time = end - start
    print(f"\nВремя выполнения программы {work_time}")