import socket
import os
import shutil

MY_DIRECT = os.path.join(os.getcwd(), 'docs')  # текущая директория


def proc(value):
    if value.startswith('help'):
        return ('pwd - название директории\n' +
                'all - содержимое директории\n' +
                'read - показать содержимое файла \n' +
                'create - создает новую папку\n' +
                'delete - удаление папки или файла\n' +
                'superdel - принудительное удаление\n' +
                'touchf - создает файл\n' +
                'pcf  - копирует файл на сервер\n' +
                'icf  - копирует файл с сервера\n' +
                'rename  - переименовывет файл\n' +
                'exit - выход')

    if value.startswith('pwd'):
        return MY_DIRECT

    elif value.startswith('all'):
        return '; '.join(os.listdir(MY_DIRECT))

    elif value.startswith('read'):
        if log in login:
            try:
                f = open(MY_DIRECT + "/" + value.replace("read ", ""), "r")
                lines = f.read()
                return lines
            except Exception:
                return "Файла не существует."
        else:
            return "У вас нет доступа"

    elif value.startswith('create'):
        if log in login:
            try:
                os.mkdir(MY_DIRECT + "/" + value.replace("create ", ""))
                return "Папка успешно создана."
            except Exception:
                return "Папки не существует."
        else:
            return "У вас нет доступа"

    elif value.startswith('delete'):
        if log in login:
            try:
                if "." in value.replace("delete ", ""):
                    os.remove(MY_DIRECT + "/" + value.replace("delete ", ""))
                    return "Удаление файла прошло успешно."
                else:
                    shutil.rmtree(MY_DIRECT + "/" + value.replace("delete ", ""))
                    return "Удаление папки прошло успешно."
            except Exception:
                return "Файл или директория не найдены"
        else:
            return "У вас нет доступа"

    elif value.startswith('superdel'):  # моментальное удаление папки
        if log in login:
            k = MY_DIRECT + "/" + value.replace("superdel ", "")
            shutil.rmtree(k, ignore_errors=False, onerror=None)
            return "Папка удалена"
        else:
            return "У вас нет доступа"

    elif value.startswith('touchf'):
        if log in login:
            try:
                # вместо имени файла не должно быть пробела
                if value.replace("touchf ", "") != value.replace("touchf ", "").startswith(" "):
                    with open(MY_DIRECT + "/" + value.replace("touchf ", ""), "w"):
                        pass
                    return "Файл успешно создан."
                else:
                    return "Недопустимое имя файла"
            except Exception:
                return "Папки не существует или в названии присутствуют неопустимые символы."
        else:
            return "У вас нет доступа"

    elif value.startswith('pcf'):  # копирует файл на сервер
        k = MY_DIRECT + "/" + value.replace("pcf ", "")
        a = os.getcwd()
        try:
            shutil.copy(k, a)
            return "Файл скопирован на сервер "
        except:
            return "Файла не существует"

    elif value.startswith('icf'):  # копирует файл с сервера
        k = MY_DIRECT + "/" + value.replace("icf ", "")
        a = os.path.join(os.getcwd(), value.replace("icf ", ""))
        try:
            shutil.copy(a, k)
            return "Файл скопирован с сервера"
        except:
            return "Файла не существует"

    elif value.startswith('rename'):
        if log in login:
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
        else:
            return "У вас нет доступа"

    elif value.startswith('exit'):
        return "Выход..."


port = 8080

sock = socket.socket()
sock.bind(('', port))
sock.listen()
print(port)
log = str(input("логин: "))
while True:
    conn, addr = sock.accept()
    login = []
    with open('login.txt', 'r') as file:
        login = file.read().splitlines()
    value = conn.recv(1024).decode()
    print(value)
    res = proc(value)
    if res.startswith('exit'):
        conn.close()
    conn.send(res.encode())

conn.close()
