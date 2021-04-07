import socket
import threading
import time

from tqdm import tqdm

mylist = []

def scan_port(ip,port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(0.5)
  try:
     connect = sock.connect((ip,port))
     print('Port :',port,' its open.')
     mylist.append(port) # записываю все порты, чтобы сделать progress bar
     connect.close()
  except:
     pass

ip = '127.0.0.1'
for i in range(1000):
 potoc = threading.Thread(target=scan_port, args=(ip,i))
 potoc.start()


# progress bar

for i in tqdm(mylist):
    time.sleep(1)