import os
import shutil
import random


def main():
    print(f"Имя ОС: {os.name}")
    print(f"Текущий путь: {os.getcwd()}")

    files = [f for f in os.listdir() if os.path.isfile(f)]

    extensions = {}
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext not in extensions:
            extensions[ext] = []
        extensions[ext].append(file)

    for ext, file_list in extensions.items():
        if ext:
            folder_name = ext[1:] + "_files"
            os.makedirs(folder_name, exist_ok=True)

            total_size = 0
            moved_count = 0

            for file in file_list:
                file_size = os.path.getsize(file)
                total_size += file_size
                shutil.move(file, os.path.join(folder_name, file))
                moved_count += 1

            size_gb = total_size / (1024 ** 3)
            print(f"В папке '{folder_name}' перемещено {moved_count} файлов, "
                  f"их суммарный размер – {size_gb:.2f} гигабайт")

    # Переименовываем случайный txt файл
    #
    if '.txt' in extensions:
        txt_folder = 'txt_files'
        if os.path.exists(txt_folder):
            txt_files = os.listdir(txt_folder)
            if txt_files:
                # Выбираем случайный файл
                #
                old_name = random.choice(txt_files)
                new_name = "renamed_" + old_name
                old_path = os.path.join(txt_folder, old_name)
                new_path = os.path.join(txt_folder, new_name)
                os.rename(old_path, new_path)
                print(f"Случайный файл {old_name} был переименован в {new_name}")


if __name__ == "__main__":
    main()