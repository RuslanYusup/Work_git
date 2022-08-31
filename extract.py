import os
import requests
import csv
import tempfile
from zipfile import ZipFile


"""
Скрипт для создания скачивания и размещения файлов из источника
"""

# установка
base_path = os.path.abspath(__file__ + "/../../")

#внешняя ссылка
source_url = "https://assets.datacamp.com/production/repositories/5899/datasets/66691278303f789ca4acd3c6406baa5fc6adaf28/PPR-ALL.zip"
# путь, где мы хотим сохранить скаченный файл
source_path =  f"{base_path}/data/source/downloaded_at=2021-01-01/ppr-all.zip" #C:\Users\user\Desktop\Work_git

raw_path = f"{base_path}/data/raw/downloaded_at=2021-02-01/ppr-all.csv"

# Создаем новую директорию
def create_folder_if_not_exists(path):
    """
    Создаем новую директорию если она не создана
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def download_snapshot():
    """
    Скачиваем новый датасет с ресурса

    """
    create_folder_if_not_exists(source_path)
    with open(source_path, "wb") as source_ppr:
        response = requests.get(source_url, verify=False)
        source_ppr.write(response.content)

def save_new_raw_data():
    """
    Сохраняем сырые данные из источника
    """
    create_folder_if_not_exists(raw_path)
    with tempfile.TemporaryDirectory() as dirpath:
        with ZipFile(
                source_path,
                "r",
        ) as zipfile:
            names_list = zipfile.namelist()
            csv_file_path = zipfile.extract(names_list[0], path=dirpath)
            # открываем файл
            with open(csv_file_path, mode="r", encoding="windows-1252") as csv_file:
                reader = csv.DictReader(csv_file)

                row = next(reader)  # получаем первую строчку
                print("[Extract] First row example:", row)

                # открываем файл для записи
                with open(
                        raw_path,
                        mode="w",
                        encoding="windows-1252"
                ) as csv_file:
                    # даем навые имена столбцам
                    fieldnames = {
                        "Date of Sale (dd/mm/yyyy)": "date_of_sale",
                        "Address": "address",
                        "Postal Code": "postal_code",
                        "County": "county",
                        "Price (€)": "price",
                        "Description of Property": "description",
                    }
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    # записываем заглавия?
                    writer.writerow(fieldnames)
                    for row in reader:
                        # записывыем все строки
                        writer.writerow(row)

# Основные функции вызываемые внутри скрипта execute.py
def main():
    print("[Extract] Start")
    print("[Extract] Downloading snapshot")
    download_snapshot()
    print(f"[Extract] Saving data from '{source_path}' to '{raw_path}'")
    save_new_raw_data()
    print(f"[Extract] End")