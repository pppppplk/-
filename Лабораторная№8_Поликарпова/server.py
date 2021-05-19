import socket

"""
Протокол Диффи-Хеллмана
"""
g = 120
a = 67
p = 100


def algorithm(g, a, p):
    key_full = g ** a % p
    return key_full


"""
проверка ключа
"""


def check(key_publ_s):
    i = False
    file = open("key_list.txt", "r")
    for line in file:
        if line[0] == str(key_publ_s):
            i = True
    return i


"""
кодирование с помощью сдвига  вправо по числовому значению символа
"""


def coding(st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])  # ord - числовое представление символа
        j += key
        j = chr(j)  # chr - возвращает символ по его числовому значению
        s[i] = j

    return ''.join(s)


"""
декодирование с помощью сдвига  влево по числовому значению символа
"""


def decoding(st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j -= key
        j = chr(j)
        s[i] = j
    return ''.join(s)


"""
генерирование ключа и шифрование сообщения
"""


def generate(a, p):
    """
    открытый ключ
    """
    publicKey = int(conn.recv(1024))  # получение сообщение
    if check(publicKey):
        msg = str(p)
        conn.send(msg.encode())
    else:
        print("Некорректный ключ")

    """
    закрытый ключ
    """
    key_part_s = int(conn.recv(1024))
    key_part_m = algorithm(publicKey, a, p)
    msg = str(key_part_m)
    conn.send(msg.encode())

    """
    зашифрованное сообщение
    """

    key_full_s = int(conn.recv(1024))
    key_full_m = algorithm(key_part_s, a, p)
    msg = str(key_full_m)
    conn.send(msg.encode())
    print(key_full_s)
    with open("keys_server.txt", "w") as file:
        file.write(str(key_full_m))

    return key_full_m


"""
получение сообщения, вывод закодированного сообщения
и отправка сообщения
"""


def mess(conn, key_full_m):
    msg = conn.recv(1024).decode()
    msg_new = decoding(msg, key_full_m)
    print("сообщение от клиента: ", msg_new)
    msg1 = input("введите сообщение: ")
    msg_new1 = coding(msg1, key_full_m)
    print("закодированное сообщение: ", msg_new1)
    conn.send(msg_new1.encode())
    return msg_new


"""
получение сообщения от клиента 
ввод сообщения от сервера
"""


def new_port(conn, keyFullMess, port):
    message = conn.recv(1024).decode()
    messageOfClient = decoding(message, keyFullMess)  # декодирую сообщение от клиента
    print("сообщение от клиента: ", messageOfClient)
    messageReceived = str(port)
    print("введите сообщение: ", messageReceived)
    messageOfServer = coding(messageReceived, keyFullMess)
    conn.send(messageOfServer.encode())  # кодирование сообщения сервера


"""
вывод порта по хосту
"""


def scanner(host_str):
    sock = socket.socket()
    for i in range(1024, 65536):
        try:
            sock.bind((host_str, i))
            scanPort = i
            sock.close()
            return scanPort
        except socket.error:
            pass


host = 'localhost'
port = scanner(host)
print(port)
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(3)

conn, addr = sock.accept()
print("соединение прошло успешно, ", addr)


try:
    with open("keys_server.txt", "r") as file:
        for line in file:
            keyFullMess = int(line)
except:
    keyFullMess = generate(a, g)

new_port(conn, keyFullMess, port)
sock.close()
sock = socket.socket()
sock.bind((host, int(port)))
sock.listen(1)
conn, addr = sock.accept()

while True:
    mess(conn, keyFullMess)

sock.close()
