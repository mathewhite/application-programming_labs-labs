import argparse
import cv2
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

def create_dataframe(data_path: str) -> pd.DataFrame:
    """
    Функция создаёт Pandas DataFrame, содержащий информацию о путях к изображениям по scv файлу.
    :param data_path: Путь к scv файлу.
    :return pd.DataFrame: Pandas DataFrame с двумя столбцами absolute_path и relative_path.
    """
    df = pd.read_csv(data_path)
    df.columns=['absolute_path','real_path']
    return df

def add_image_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет информацию о размерах и цветовой глубине изображений в существующий DataFrame.
    :param pd.DataFrame: Pandas DataFrame, который содержит столбец с именем 'absolute_path', где хранятся абсолютные пути к файлам изображений
    :return pd.DataFrame: Изменённый DataFrame. К исходному DataFrame добавляются три новых столбца, содержащие высоту, ширину и количество цветовых каналов соответственно для каждого изображения.
    """
    heights = []
    widths = []
    depths = []

    for path in df['absolute_path']:
        img = cv2.imread(path)
        if img is None:
            print(f"Failed to load image: {path}. Check the path!")
            heights.append(None)
            widths.append(None)
            depths.append(None)
        else:
            heights.append(img.shape[0])
            widths.append(img.shape[1])
            depths.append(img.shape[2])

    df['height'] = heights
    df['width'] = widths
    df['depth'] = depths
    return df

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет описательную статистику для числовых столбцов 'height', 'width' и 'depth'.
    :param df (pd.DataFrame)`: Входной Pandas DataFrame
    :return pd.DataFrame: Pandas DataFrame, содержащий описательную статистику для столбцов 'height', 'width' и 'depth'.
    """
    stats = df[['height', 'width', 'depth']].describe()
    return stats

def filter_images(df: pd.DataFrame, max_width: int, max_height: int) -> pd.DataFrame:
    """
    Фильтрует DataFrame, оставляя только строки, соответствующие заданным максимальным значениям высоты и ширины изображения.
    :param pd.DataFrame: Входной Pandas DataFrame, содержащий столбцы 'height' и 'width' с числовыми данными.
            max_width: Максимально допустимая ширина изображения.
            max_height: Максимально допустимая высота изображения.
    :return pd.DataFrame: Новый Pandas DataFrame.
    """
    return df[
        (df['height'] <= max_height) &
        (df['width'] <= max_width)
    ]

def add_image_area(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет в DataFrame информацию о площади изображения и упорядочивает строки по возрастанию площади.
    :param pd.DataFrame: Входной Pandas DataFrame
    :return pd.DataFrame: Pandas DataFrame, содержащий все столбцы исходного DataFrame, плюс новый столбец 'area', содержащий площади изображений
    """
    df['area'] = df['height'] * df['width']
    df = df.sort_values(by='area').reset_index(drop=True)
    return df

def plot_area_distribution(df: pd.DataFrame) -> None:
    """
    Строит гистограмму распределения площадей изображений.
    :param pd.DataFrame: Pandas DataFrame, содержащий столбец 'area' с числовыми данными.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(df['area'], bins=20, edgecolor='black')
    plt.title("Распределение площадей изображений")
    plt.xlabel("Площадь изображения (пиксели)")
    plt.ylabel("Количество изображений")
    plt.show()

def main(data_path: str, max_width: int, max_height: int) -> None:
    df = create_dataframe(data_path)
    df = add_image_info(df)
    stats = calculate_statistics(df)
    filtered_df = filter_images(df, max_width, max_height)
    print("\nФильтрованные данные по заданным диапазонам размеров:")
    print(filtered_df)
    df = add_image_area(df)
    plot_area_distribution(df)
    print("\nСтатистика по высоте, ширине и глубине изображений:")
    print(stats)
    print("\nИтоговый DataFrame:")
    print(df.head(len(df)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Анализ изображений и их фильтрация по диапазону размеров.")
    parser.add_argument("--data_path", type=str, required=True, help="Путь к scv файлу с путями к изображениям")
    parser.add_argument("--max_width", type=int,help="Максимальная ширина изображения")
    parser.add_argument("--max_height", type=int, help="Максимальная высота изображения")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(f"Ошибка в аргументах: {e}")
        parser.print_help()
        sys.exit(1)

    main(args.data_path, args.max_width, args.max_height)
