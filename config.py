import json
import sys
import os

# os.chdir(sys._MEIPASS)


def get_config():
    try:
        with open("config.json") as file:
            config = json.load(file)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        raise e

    return config
