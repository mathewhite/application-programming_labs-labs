import argparse
import re

def parsing() -> str:
    """
    добавляет аргумент при запуске через командную строку 
    и возвращает введенный аргумент 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='name of file')
    return parser.parse_args().name

def file_reading(name: str) -> str:
    """
    получает имя файла который нужно открыть 
    и возвращает содержание этого файла 
    в виде строки
    """
    try:
        with open(f"{name}", "r", encoding="utf-8") as file:
            text= file.read()
            return text
    except:
        raise FileExistsError("Некорректный файл")

def making_list(text: str) -> list:
    """
    разбивает анкеты на список 
    """
    return re.split(r"\n{2}",text)

def sorting(data: list) -> list:
    """
    получает список анкет, 
    возвращет список анекет людей 
    с фамилией Иванов(а)
    """
    lst= list()
    for item in data:
        if re.search("Фамилия: Иванов"+r"а?", item) :
            lst.append(i)
        else:
            continue
    return lst

if __name__ == "__main__":
    try:
        name_of_file= parsing()
        full_file=file_reading(name_of_file)
        list_all= making_list(full_file)
        list_ivanovs= sorting(list_all)
        for i in list_ivanovs:
            print (i)
    except FileExistsError as exc:
        print(exc)






