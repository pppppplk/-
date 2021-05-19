import socket

"""
Протокол Диффи-Хеллмана
a, g, p = любые числа 
"""
a = 100
g = 104
p = 78


def algorithm(a, g, p):
    key_full = g ** a % p
    return key_full


"""
кодирование с помощью сдвига по числовому значению символа
"""


def coding(st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j += key
        j = chr(j)
        s[i] = j
    return ''.join(s)


def decoding(st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j -= key
        j = chr(j)
        s[i] = j
    return ''.join(s)


def generate(a, g):
    """
    открытый ключ
    """
    msg = str(a)
    sock.send(msg.encode())
    try:
        publicKey = int(sock.recv(1024))
    except ValueError:
        print("Неверный ключ.")

    """
    закрытый ключ
    """
    key_part_m = algorithm(g, a, publicKey)
    msg = str(key_part_m)
    sock.send(msg.encode())
    key_part_s = int(sock.recv(1024))

    """
    зашифрованное сообщение
    """
    key_full_m = algorithm(key_part_s, a, publicKey)
    print(key_part_s, a, publicKey)
    msg = str(key_full_m)
    sock.send(msg.encode())
    key_full_s = int(sock.recv(1024))
    with open("keys_client.txt", "w") as file:
        file.write(str(key_full_s))
    return key_full_s


def mess(sock, keyFullMess):
    msg = input('введите сообщение: ')
    msg_new = coding(msg, keyFullMess)
    print("закодированное", msg_new)
    sock.send(msg_new.encode())
    msg = sock.recv(1024).decode()
    msg_new = decoding(msg, keyFullMess)
    print("сообщение от сервера: ", msg_new)
    return msg_new


host = 'localhost'
sock = socket.socket()
sock.setblocking(1)
sock.connect((host, 9090))
print("соединение прошло успешно ")

try:
    with open("keys_client.txt", "r") as file:
        for line in file:
            keyFullSer = int(line)
except:
    keyFullSer = generate(a, g)

port = mess(sock, keyFullSer)
sock.close()
sock = socket.socket()
sock.connect((host, 1024))

while True:
    mess(sock, keyFullSer)
sock.close()
