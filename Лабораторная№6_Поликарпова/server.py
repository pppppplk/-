import datetime, http.server, socketserver, http.client, requests

list = []
with open('info.txt', 'r') as file:
    list = file.read().splitlines()

port = int(list[0])
err = 'ошибок нет'
if len(list) > 1:
    file = str(list[1])
    a = file.find('.')
    type_file = file[a + 1:]
    if type_file == 'html' or type_file == 'css' or type_file == 'jpg':
        print("work")
    else:
        err = 'Error 403'
        file = '2.html'
else:
    err = 'Error 404'
    file = '1.html'


# запуск простого HTTP-сервера
class ReqHand(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = file
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# информация
handler = ReqHand
with socketserver.TCPServer(("", port), handler) as httpd:
    info = ("Дата: " + str(datetime.datetime.now()) +
            "\nПорт: " + str(port) +
            "\nНазвание файла: " + file +
            "\nОшибка: " + str(err))

    print(info)
    res = requests.get('https://scotch.io')

    # вывод заголовков сайта
    print("Заголовки сайта: ")
    for item in res.headers.items():
        print(item)

    httpd.serve_forever()
