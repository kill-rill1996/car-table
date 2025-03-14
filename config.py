import json


def get_config():
    try:
        with open("config.json") as file:
            config = json.load(file)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        raise e

    return config
