import socket, threading
import logging


def get_logger():
    """
    Функция вывода служебных сообщений в специальный лог-файл

    """

    # создаем объект логирования, называем его server
    logger = logging.getLogger("server2")

    # будет отображать логи, где все идет хорошо и без ошибок
    logger.setLevel(logging.INFO)

    # куда будем записывать логи
    file_hanlder = logging.FileHandler("server2.log")

    # применяем желаемое для логирования отформатирование
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # устанавливаем данное форматирование для хэндлера
    file_hanlder.setFormatter(formatter)

    # добавляем данный хендлер к нашему объекту логирования
    logger.addHandler(file_hanlder)

    return logger


logger = get_logger()
logger.info('Сервер запущен')
sock = socket.socket()

HOST = 'localhost'
PORT = 9090
logger.info(f'Начало прослушивание порта {str(PORT)}')

# Вводим имя для чата
uname = input('Введите имя  > ')
logger.info(f'пользователь {uname} отправил сообщение')

"""
создание сокета (по нему устанавливается соединение, обе стороны ведут разговор до тех
пор пока не будет прервано)
"""

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Функция отправки сообщений с определенным началом
def send(uname):
    while True:
        mess = input(f'\n {uname} > ')
        data = uname + '>' + mess
        cli_sock.send(bytes(data, encoding="utf-8"))
        logger.info(f'текст сообщения:  {mess} ')


# функция принятия сообщений
def receive():
    while True:
        data = cli_sock.recv(1024)
        print('\t' + str(data))
        if data:
            print("Приняты данные от сервера: " + data.decode())
        else:
            logger.info(f'сервер разорвал соединение')
            break


if __name__ == "__main__":
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cli_sock.connect((HOST, PORT))

    """
    создаем новый поток и запускаем его 
    (потоку даем имя, которое пользователь выбрал для себя для чата)
    """

    thread_send = threading.Thread(target=send, args=[uname])
    thread_send.start()

    # начинаем получать данные
    thread_receive = threading.Thread(target=receive)
    thread_receive.start()
