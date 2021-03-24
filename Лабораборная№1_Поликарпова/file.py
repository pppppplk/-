
import os
import configparser
import shutil


config = configparser.ConfigParser()
config.read('config.ini')


ROOT_DIRECT = config["settings"]["WORKING_DIRECTORY"]
MY_DIRECT = config["settings"]["WORKING_DIRECTORY"]  # текущая директория

"""
функция создание папки 
"""
def create_f(value):
    try:
        os.mkdir(MY_DIRECT + "/" + value.replace("create ", ""))
        print("Папка успешно создана.")
    except Exception:
        print("Папки не существует.")


"""
функция удаления папки или файла
"""

def delete_f(value):

    try:
        if "." in value.replace("delete ", ""):
            os.remove(MY_DIRECT + "/" + value.replace("delete ", ""))
            print("Удаление файла прошло успешно.")
        else:
            shutil.rmtree(MY_DIRECT + "/" + value.replace("delete ", ""))
            print("Удаление папки прошло успешно.")
    except Exception:
        print("Файл или директория не найдены")




"""
функция перехода между директориями
"""
def cd_f(value, cur_dir):
    if len(value) == 12 and value[11] == value[10] == ".":  # cd ..
        if cur_dir != ROOT_DIRECT:
            temp = cur_dir[:cur_dir.rfind("/")]
            os.chdir(temp) # смена директории
            cur_dir = temp
            return cur_dir
    elif len(value) > 11 and value[10] == " ":
        try:
            temp = cur_dir + "/" + value.replace("transition ", "")
            os.chdir(temp)
            cur_dir = temp
            return cur_dir
        except Exception:
            print("Нет такой директории. Введите all для посмотра содержания текущей директории.")
            return cur_dir
    else:
        return cur_dir

"""
функция создания файла
"""
def touch_f(value):

    try:
        # вместо имени файла не должно быть пробела
        if value.replace("touchf ", "") != value.replace("touchf ", "").startswith(" "):
            with open(MY_DIRECT + "/" + value.replace("touchf ", ""), "w"):
                pass
            print("Файл успешно создан.")
        else:
            print("Недопустимое имя файла")
    except Exception:
        print("Папки не существует или в названии присутствуют неопустимые символы.")

"""
функция записи в файл
"""
def write_f(value):

    try:
        name = value.replace("write ", "")
        text = name[name.find(" ") + 1:]  # выделяем значения после пробела
        name = name[:name.find(" ")] # команда знач (выделяем до пробела)
        with open(MY_DIRECT + "/" + name, "a+") as f:
            f.write("\n" + text)
        print("Данные записаны.")
    except Exception:
        print("Файла не существует.")

"""
функция чтения  файла
"""
def read_f(value):

    try:
        f = open(MY_DIRECT + "/" + value.replace("read ", ""), "r")
        lines = f.read()
        print(lines)
    except Exception:
        print("Файла не существует.")

"""
функция копирования файла или папки
"""
def copy_f(value):

    try:
        name = value.replace("copy ", "")
        file1 = name[:name.find(" ")]
        name = name.replace(file1 + " ", "")
        file2 = name
        if "/" not in file1 and "/" not in file2:
            shutil.copyfile(MY_DIRECT + "/" + file1, MY_DIRECT + "/" + file2)
        else:
            if "/" in file1 and "/" in file2 and ROOT_DIRECT in file1 and ROOT_DIRECT in file2:
                shutil.copyfile(file1, file2)
            else:
                print("Данные не могут быть скопированы, директории или файлы не найдены")
    except Exception:
        print("Файла не существует.")

"""
функция перемещения файла 
"""
def move_f(value):

    try:

        value.replace("move ", "")
        name = value.replace("move ", "")
        file1 = name[:name.find(" ")]
        name = name.replace(file1 + " ", "")
        file2 = name
        if "/" in file2 and ROOT_DIRECT in file2:
            if "/" in file1 and ROOT_DIRECT in file1:
                shutil.move(file1, file2)
            elif "/" != file1:
                shutil.move(MY_DIRECT + "/" + file1, file2)
        else:
            print("Место назначения должно быть директорией с прописанным путем.")
    except Exception:
        print("Файла не существует.")

"""
функция переименования файла 
"""
def rename_f(value):

    try:
        name = value.replace("rename ", "")
        file1 = name[:name.find(" ")]
        name = name.replace(file1 + " ", "")
        file2 = name
        if "/" != file1 and "/" != file2:
            os.rename(MY_DIRECT + "/" + file1, MY_DIRECT + "/" + file2)
            print("Файл переименован")
        else:
            print("Файла не существует.")
    except Exception:
        print("Файла не существует.")




while True:
    try:
        value = input("$"+MY_DIRECT +">")
        if value.startswith("create "):
            create_f(value)

        elif value.startswith("delete "):
            delete_f(value)

        elif value.startswith("transition"):
            result = cd_f(value, MY_DIRECT)
            MY_DIRECT = result

        elif value.startswith("touchf "):
            touch_f(value)

        elif value.startswith("write "):
           write_f(value)

        elif value.startswith("read "):
            read_f(value)
        elif value.startswith("copy "):
           copy_f(value)
        elif value.startswith("move "):
            move_f(value)
        elif value.startswith("rename "):
           rename_f(value)

        elif value == "all":
            for file in os.listdir(path=MY_DIRECT):
                print(file)
        elif value == "help":
            print("create - создание папки\ndelete - удаление папки или файла\ntransition - переход между директориями"
                  "\ntouchf - создание файла\nwrite - запись в файл\nread - чтение файла\ncopy - копирование файла"
                  "\nmove - перемещение файла\nrename - переименование файла\nall - все файлы и папки каталога")
        else:
            print("Такой команды нет. Введите help, чтобы узнать доступные команды")
    except KeyboardInterrupt as e:
        break


