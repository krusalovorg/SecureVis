import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
import string
import random
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)
# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Security_db']

# Коллекция для администраторов
admins_collection = db['admins']

# Коллекция для сотрудников
staff_collection = db['staff']
enterprises_collection = db['enterprises_collection']


# add to db
def add_to_database(data, db):
    if db == 'admins':
        admins_collection.insert_one(data)
    elif db == 'staff':
        staff_collection.insert_one(data)
    elif db == 'enterprise':
        enterprises_collection.insert_one(data)


def generate_unique(word, why):
    while True:
        login = word  # Ваше желаемое начальное имя логина
        numbers = ''.join(random.choice(string.digits) for _ in range(3))  # Генерируем случайные цифры
        unique = login + numbers
        if why == 'login':
            if staff_collection.find_one(
                    {'login': unique}) is None:  # Проверяем, существует ли такой логин в базе данных
                return unique
        elif why == 'password':
            if staff_collection.find_one(
                    {'password': unique}) is None:  # Проверяем, существует ли такой логин в базе данных
                return unique


@app.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    password = data['password']
    email = data['email']
    user = admins_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'incorrect password'}), 401


@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json()
    password = data['password']
    login = data['login']
    user = staff_collection.find_one({'login': login})
    if user and check_password_hash(user['password'], password):
        current_time = datetime.now()
        day = current_time.strftime("%d.%m.%Y")  # Форматируем текущую дату в соответствии с требуемым форматом

        # Обновляем настройки пользователя в базе данных
        update_query = {
            f"settings.{day}.time_log": current_time.strftime("%H:%M")
        }
        staff_collection.update_one({'login': login}, {'$set': update_query})

        access_token = create_access_token(identity=login)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'incorrect password'}), 401



@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    data = request.get_json()
    login = data['login']
    user = staff_collection.find_one({"login": get_jwt_identity()})

    if user:
        current_time = datetime.now()
        day = current_time.strftime("%d.%m.%Y")  # Форматируем текущую дату в соответствии с требуемым форматом

        # Получаем время начала работы из настроек
        start_time = datetime.strptime(user['settings'][day]['time_log'], "%H:%M")

        # Получаем время окончания работы
        end_time = current_time.strftime("%H:%M")

        # Рассчитываем время работы
        work_time = (current_time - start_time).seconds // 3600

        # Обновляем настройки пользователя в базе данных
        update_query = {
            f"settings.{day}.end_time": end_time,
            f"settings.{day}.work_time": work_time
        }
        staff_collection.update_one({'login': login}, {'$set': update_query})

        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404



@app.route('/register_staff', methods=['POST'])
@jwt_required()
def register_staff():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    patronymic = data.get('patronymic')
    position = data.get('position')
    statistic = []
    timetable = data.get('timetable')
    worktime = data.get('worktime')
    org_id = data.get("org_id")
    photo = request.files['photo'] if 'photo' in request.files else None

    login = generate_unique(name, 'login')
    password = generate_unique(surname, 'password')
    print(f'password - {password} , login - {login}')
    if photo:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(photo_path)
    else:
        photo_path = None

    add_to_database(
        {'name': name, 'surname': surname, 'patronymic': patronymic, 'position': position, 'statistic': statistic,
         'timetable': timetable,
         'worktime': worktime, 'login': login, 'password': generate_password_hash(password, method='pbkdf2:sha256'),
         'org_id': org_id, 'photo_path': photo_path},
        'staff')

    return jsonify({'message': 'User registered successfully'}), 200



@app.route('/update_staff', methods=['PUT'])
@jwt_required()
def update_staff():
    data = request.get_json()
    updated_fields = {}
    # Обновляем только поля, которые были переданы
    for key in data:
        updated_fields[key] = data[key]

    # Удаляем поля, которые не нужно обновлять
    updated_fields.pop('_id', None)
    updated_fields.pop('login', None)
    updated_fields.pop('password', None)

    staff_collection.update_one({'_id': data.get('id')}, {'$set': updated_fields})
    return jsonify({'message': 'Staff updated successfully'}), 200



@app.route('/get_staff', methods=['GET'])
@jwt_required()
def get_staff():
    data = request.get_json()
    staff = staff_collection.find_one({'_id': data.get('id')})
    if staff:
        return jsonify(staff), 200
    else:
        return jsonify({'message': 'Staff not found'}), 404



@app.route('/get_staffs', methods=['GET'])
@jwt_required()
def get_staffs():
    data = request.get_json()
    staffs = staff_collection.find({'org_id': data.get('org_id')})
    return jsonify(staffs), 200



@app.route('/get_enterprise', methods=['GET'])
@jwt_required()
def get_enterprise():
    data = request.get_json()
    enterprise = enterprises_collection.find_one({'_id': data.get('id')})
    if enterprise:
        return jsonify(enterprise), 200
    else:
        return jsonify({'message': 'Enterprise not found'}), 404



@app.route('/add_enterprise', methods=['POST'])
@jwt_required()
def add_enterprise():
    data = request.get_json()
    add_to_database(data, 'enterprise')
    return jsonify({'message': 'Enterprise added successfully'}), 200


@app.route('/update_enterprise', methods=['PUT'])
def update_enterprise():
    data = request.get_json()
    updated_fields = {}
    for key in data:
        updated_fields[key] = data[key]

    enterprises_collection.update_one({'_id': data.get('id')}, {'$set': updated_fields})
    return jsonify({'message': 'Enterprise updated successfully'}), 200



@app.route('/get_enterprises', methods=['GET'])
@jwt_required()
def get_enterprises():
    enterprises = enterprises_collection.find()
    return jsonify(enterprises), 200


def addAdminUser():
    new_user_data = {
        "email": "admin@admin.admin",
        "name": "admin"
    }

    # Поиск пользователя по email
    existing_user = admins_collection.find_one({"email": new_user_data["email"]})

    if not existing_user:
        # Генерация хеша пароля
        hashed_password = generate_password_hash('123456', method='pbkdf2:sha256')
        new_user_data["password"] = hashed_password
        # Добавление пользователя в коллекцию
        admins_collection.insert_one(new_user_data)
        print("Пользователь успешно добавлен. Пароль:", '123456')
    else:
        print("Пользователь уже существует в базе данных.")


if __name__ == '__main__':
    addAdminUser()
    app.run(debug=True)
