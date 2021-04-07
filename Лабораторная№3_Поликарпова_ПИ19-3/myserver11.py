# сервер потоками
import socket, threading


conect_user = []  # список подключенных к чату



def accept():
    # Функция регистрации и подключения клиента
    while True:
        cli_sock, cli_add = sock.accept()
        conect_user.append(cli_sock)  # добавляем клиента в наш список

        # создаем новый поток для этого клиента
        thread_client = threading.Thread(target=broadcast_usr, args=[cli_sock])

        thread_client.start()  # запускаем новый поток


def broadcast_usr(cli_sock):
    # Функция ответа клиенту
    while True:
        try:
            data = cli_sock.recv(1024)  # запрос

            if data:
                for client in conect_user:
                    # и отправляем сообщение всем, кроме отправителя
                    if client != cli_sock:
                        client.send(data)

        except Exception as x:
            print(x.message)
            break



"""
создание сокета (по нему устанавливается соединение, обе стороны ведут разговор до тех
пор пока не будет прервано)
"""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 9090
sock.bind((host, port))

sock.listen(1)
print('Чат соединен с портом : ' + str(port))

# Создаем новый поток и запускаем его
thread_ac = threading.Thread(target=accept)
thread_ac.start()


