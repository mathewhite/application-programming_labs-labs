import argparse
import re

def parsing() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='name of file')
    return parser.parse_args().name

def file_reading(name: str) -> str:
    try:
        with open(f"{name}", "r", encoding="utf-8") as file:
            text= file.read()
            return text
    except:
        raise FileExistsError("Некорректный файл")

def making_list(text: str) -> list:
    return re.split(r"\n{2}",text)

def sorting(data: list) -> list:
    lst= list()
    for item in data:
        if re.search("Фамилия: Иванов"+r"а?", item) :
            lst.append(i)
        else:
            continue
    return lst

if __name__ == "__main__":
    try:
        for i in sorting(making_list(file_reading(parsing()))):
            print(i)
    except FileExistsError as exc:
        print(exc)






