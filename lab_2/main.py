import os
import csv
import argparse
from icrawler.builtin import GoogleImageCrawler


def download_images(keyword: str, save_dir: str, max_images: int=100)->None:
    """
    Загружает изображения по указанному ключевому слову.
    :param:
    keyword: строка с ключевым словом для поиска изображений.
    save_dir: строка, указывающая каталог, в который будут сохранены изображения.
    max_images: максимальное количество загружаемых изображений.
    :return: None
    """
    os.makedirs(save_dir, exist_ok=True)

    google_crawler = GoogleImageCrawler(storage={'root_dir': save_dir})
    google_crawler.crawl(keyword=keyword, max_num=max_images)

def create_annotation(save_dir: str, annotation_file: str) -> None:
    """
    Cоздает аннотацию для загруженных изображений.
    :param:
    save_dir: строка, указывающая каталог, в который будут сохранены изображения.
    annotation_file: строка, указывающая путь к файлу, в который будет записана аннотация.
    :return: None
    """
    with open(annotation_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["absolute_path", "relative_path"])

        for root, _, files in os.walk(save_dir):
            for filename in files:
                abs_path = os.path.abspath(os.path.join(root, filename))
                rel_path = os.path.relpath(abs_path, save_dir)
                writer.writerow([abs_path, rel_path])


class ImageIterator:
    def __init__(self, annotation_file: str=None, image_dir: str=None)->None:
        """
         Инициализирует объект, загружая пути к изображениям
         :param:annotation_file строка с путем к файлу аннотации.
                image_dir строка с путем к директории, содержащей изображения.
         :return: None
         """
        self.image_paths = []

        if annotation_file:

            with open(annotation_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                self.image_paths = [row[0] for row in reader]
        elif image_dir:
            for root, _, files in os.walk(image_dir):
                for filename in files:
                    abs_path = os.path.abspath(os.path.join(root, filename))
                    self.image_paths.append(abs_path)
        else:
            raise ValueError("Specify an annotation file or directoru with images")

        self.index = 0

    def __iter__(self)->'ImageIterator':
        return self

    def __next__(self)->str:
        if self.index < len(self.image_paths):
            image_path = self.image_paths[self.index]
            self.index += 1
            return image_path
        else:
            raise StopIteration


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images and create an annotation.")
    parser.add_argument("keyword", type=str, help="Keyword for image search, e.g., 'pig'")
    parser.add_argument("save_dir", type=str, help="Directory to save images")
    parser.add_argument("annotation_file", type=str, help="CSV file for annotations")
    parser.add_argument("max_images", type=int, default=50, help="Maximum number of images to download (50-100)")

    args = parser.parse_args()

    download_images(
        keyword=args.keyword,
        save_dir=args.save_dir,
        max_images=args.max_images
    )

    create_annotation(
        save_dir=args.save_dir,
        annotation_file=args.annotation_file
    )

    print("Iterate over images:")
    iterator = ImageIterator(annotation_file=args.annotation_file)
    for image_path in iterator:
        print(image_path)