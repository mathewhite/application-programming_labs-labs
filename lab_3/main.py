import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

def load_image(input_path: str) -> np.ndarray:
    """
    Функция принимает путь к файлу изображения и возвращает изображение
    :param input_path: Строка, содержащая путь к файлу изображения
    :return: Изображение
    """
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("Ошибка: изображение не загружено.")
    return image

def display_image_info(image: np.ndarray) -> None:
    """
    Выводит информацию о размере изображения
    :param image: Многомерный массив NumPy, представляющий изображение.
    """
    if image is not None:
        print(f"Размер изображения: {image.shape}")
    else:
        print("Ошибка: изображение не загружено.")

def plot_histogram(image: np.ndarray) -> None:
    """
    Строит и отображает гистограмму интенсивностей пикселей
    :param image: Многомерный массив NumPy, представляющий изображение.
    """
    try:
        colors = ('b', 'g', 'r')
        plt.figure(figsize=(10, 5))
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=color)
            plt.xlim([0, 256])
        plt.title("Image Histogram")
        plt.xlabel("Intensity")
        plt.ylabel("Frequency")
        plt.legend(['Blue', 'Green', 'Red'])
        plt.show()
    except Exception as e:
        print(f"Ошибка при построении гистограммы: {e}")

def rotate_image(image: np.ndarray, flip_code: int) -> np.ndarray:
    """
    Отзеркаливает изображение по заданной оси
    :param image: Массив NumPy, представляющий изображение.
    :param flip_code: Целое число, задающее характер отзеркаливания: 0- по оси у, 1- по оси х, -1 - по обеим осям.
    :return: Зеркальное изображение
    """
    if image is None:
        raise ValueError("Ошибка: изображение не загружено.")
    rotated_image = cv2.flip(image, flip_code)
    return rotated_image

def display_images(original: np.ndarray, flipped: np.ndarray) -> None:
    """
    Отображает исходное и зеркальное изображения
    :param original: Массив NumPy, представляющий исходное изображение в оттенках серого.
    :param flipped: Массив NumPy, представляющий зеркальное изображение
    """
    if original is None or flipped is None:
        raise ValueError("Ошибка: одно из изображений не загружено.")

    cv2.imshow('original', original)
    cv2.imshow('rotated', flipped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def save_image(image: np.ndarray, output_path: str) -> None:
    """
    Сохраняет изображение в файл
    :param image: Массив NumPy, представляющий изображение, которое нужно сохранить.
    :param output_path: Строка, представляющая путь к файлу, куда нужно сохранить изображение.
    """
    if not output_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise ValueError("Ошибка: укажите корректное расширение файла для сохранения (.jpg, .jpeg или .png).")
    if cv2.imwrite(output_path, image):
        print(f"Изображение сохранено по пути: {output_path}")
    else:
        raise IOError("Ошибка при сохранении изображения. Проверьте путь и разрешения на запись.")

def main(input_path: str, output_path: str, flip_code: int = 1) -> None:
    """
    Основная функция для выполнения всех операций
    :param input_path: Строка, представляющая путь к файлу изображения, которое нужно обработать.
    :param output_path: Строка, представляющая путь к файлу, куда нужно сохранить отзеркаленное изображение.
    :param flip_code: Целое число, задающее характер отзеркаливания: 0- по оси у, 1- по оси х, -1 - по обеим осям.
    """
    image = load_image(input_path)
    display_image_info(image)
    plot_histogram(image)
    rotated_image = rotate_image(image, flip_code)
    display_images(image, rotated_image)
    save_image(rotated_image, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка изображения и конвертация в  отзеркаленный вид.")
    parser.add_argument("input_path", type=str, help="Путь к исходному изображению")
    parser.add_argument("output_path", type=str, help="Путь для сохранения зеркального изображения")
    parser.add_argument("flip_code", type=int, default=1, help="как развернуть изображение: 0- по оси у, 1- по оси х, -1 - по обеим осям, по умолчанию: 1")
    args = parser.parse_args()

    main(args.input_path, args.output_path, args.flip_code)
