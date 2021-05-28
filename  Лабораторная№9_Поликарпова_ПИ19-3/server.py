from flask import Flask, jsonify, abort
import json

"""
запуск фреймворка Flask
"""
app = Flask(__name__)

"""
считывание json файла
"""
users = []
with open('userList.json', 'r') as file:
    users = json.load(file)


@app.route('/')  # привязка к URL
def HomePage():
    return "Поздравляю, страница открыта!"


"""
вывод всех пользователей
"""


@app.route('/alluser/', methods=['GET'])
def GetAllUsers():
    return jsonify({'users': users})


"""
вывод пользователя по id
"""


@app.route('/user/<int:user_id>', methods=['GET'])
def GetUserById(user_id):
    user = []
    for perem in users:
        if perem["user_id"] == user_id:
            user.append(perem)

    if len(user) == 0:
        abort(404) # обработка ошибки
    return jsonify({'user': user[0]}) # возвражение json - объекта


if __name__ == '__main__':
    app.run(debug=True)
