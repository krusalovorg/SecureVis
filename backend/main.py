import asyncio
import base64
import os
import time
from io import BytesIO

from PIL import Image
from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
from datetime import datetime, timedelta
import string
import random
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import json
from flask_cors import CORS
import websockets

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '12221'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)
wsUrl = 'ws://127.0.0.1:5001'

CORS(app)

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Security_db']

# Коллекция для сотрудников
staff_collection = db['staff']
enterprises_collection = db['enterprises']


def serialize_object(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


# add to db
def add_to_database(data, db):
    if db == 'staff':
        staff_collection.insert_one(data)
    elif db == 'enterprise':
        enterprises_collection.insert_one(data)


# создание уникального login или password
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


@app.route('/staff_apps', methods=['POST'])
def staff_apps():
    data = request.json  # Получаем данные из запроса
    print(data)  # Выводим полученные данные в консоль

    # Извлекаем необходимые данные из запроса
    staff_id = data.get('id')
    apps = data.get('apps')
    if staff_id == '':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = file.filename
                path = os.path.join(app.root_path, 'images', 'unknown', filename)
                file.save(path)
                photo_path = path
                data = {"name": generate_unique('unknown', 'login'), "statistics": [], "photo_path": photo_path}
        else:
            data = {"name": generate_unique('unknown', 'login'), "statistics": [], "photo_path": None}
        add_to_database(data, 'staff')
        return 'Succes'
    else:
        # Проверяем, есть ли сотрудник с таким ID
        staff = staff_collection.find_one({"_id": ObjectId(staff_id)})
        if staff:
            # Получаем текущую дату
            current_date = datetime.now().strftime("%d:%m:%Y")

            # Проверяем, есть ли записи на текущий день в статистике
            if "statistics" not in staff or not any(entry.get('day') == current_date for entry in staff['statistics']):
                return jsonify({'message': 'No statistics available for today'}), 404

            # Получаем статистику для текущего дня
            statistics_today = next(entry for entry in staff['statistics'] if entry.get('day') == current_date)

            # Получаем словарь приложений на текущий день
            apps_today = statistics_today.get('apps', {})
            # Обновляем или добавляем время для каждого приложения из списка apps
            for app_name, app_time in apps.items():
                # Обновляем время приложения или добавляем новое приложение
                apps_today[app_name] = app_time

            # Обновляем статистику в базе данных
            staff_collection.update_one(
                {"_id": ObjectId(staff_id), "statistics.day": current_date},
                {
                    "$set": {
                        "statistics.$.apps": apps_today
                    }
                }
            )

            return jsonify({'message': 'Apps added/updated in staff statistics successfully'}), 200
        else:
            return jsonify({'message': 'Staff not found'}), 404

@app.route('/image/<org_id>/<image_name>', methods=['GET'])
def send_image(org_id, image_name):
    image_path = os.path.join(app.root_path, 'userdata', org_id, image_name)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return "Файл не найден", 404

@app.route('/user_event', methods=['POST'])
def user_event():
    data = request.get_json()
    print('connect', data)
    current_time = datetime.now()
    day = current_time.strftime("%d:%m:%Y")  # Format the current date
    id = data.get('id')
    if id != '':
        id = ObjectId(id)
        user = staff_collection.find_one({"_id": id})
        # Handle file upload if present in requests
        photo_path = None
        if 'image' in data:
            image_data = base64.b64decode(data.get("image"))
            image = Image.open(BytesIO(image_data))
            filename = f"{user.get('name')}{str(time.time()).replace('.', '')}.jpg"
            dir_path = os.path.join('userdata', str(user['org_id']))
            # Проверка наличия каталога и создание его при необходимости
            os.makedirs(dir_path, exist_ok=True)
            path = os.path.join(dir_path, filename)
            print(path)
            image.save(path, 'JPEG')
            photo_path = str(user['org_id']) + '/' + filename

        # Continue with your existing logic
        day_entry = next((entry for entry in user['statistics'] if entry['day'] == day), None)

        if day_entry is None:
            staff_collection.update_one(
                {"_id": id},
                {
                    "$addToSet": {
                        "statistics": {
                            "day": day,
                            "total_work_time": 0,
                            "logs": [{
                                "time_start": current_time.strftime("%H:%M:%S"),
                                "start_photo_path": photo_path
                            }]
                        }
                    }
                }
            )
        else:
            if 'time_end' not in day_entry['logs'][-1]:
                staff_collection.update_one(
                    {"_id": id, "statistics.day": day},
                    {
                        "$set": {
                            f"statistics.$.logs.{len(day_entry['logs']) - 1}.time_end": current_time.strftime(
                                "%H:%M:%S"),
                            f"statistics.$.logs.{len(day_entry['logs']) - 1}.end_photo_path": photo_path
                        }
                    }
                )
                time_start = datetime.strptime(day_entry['logs'][-1]['time_start'], "%H:%M:%S")
                time_end = datetime.strptime(current_time.strftime("%H:%M:%S"), "%H:%M:%S")
                work_time_seconds = (time_end - time_start).total_seconds()
                total_work_day = day_entry.get('total_work_time', 0)
                total_work_day += work_time_seconds
                staff_collection.update_one(
                    {"_id": id, "statistics.day": day},
                    {
                        "$set": {f"statistics.$.total_work_time": total_work_day}
                    }
                )

                staff_collection.update_one(
                    {"_id": id, "statistics.day": day},
                    {
                        "$set": {f"statistics.$.logs.{len(day_entry['logs']) - 1}.work_time": work_time_seconds}
                    }
                )
            else:
                staff_collection.update_one(
                    {"_id": id, "statistics.day": day},
                    {
                        "$push": {f"statistics.$.logs": {"time_start": current_time.strftime("%H:%M:%S"),
                                                         "start_photo_path": photo_path}}
                    }
                )
        return "Success"


# войти в аккаунт администратора
@app.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    password = data['password']
    email = data['email']
    print(password, email)
    user = enterprises_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'incorrect password'}), 401


# пользователю войти в аккаунт
@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json()
    if data['email']:
        password = data['password']
        email = data['email']
        user = enterprises_collection.find_one({'email': email})
        print(user)
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'incorrect password'}), 401
    else:
        password = data['password']
        login = data['login']
        user = staff_collection.find_one({'login': login})
        if user and check_password_hash(user['password'], password):
            current_time = datetime.now()
            day = current_time.strftime("%d:%m:%Y")  # Форматируем текущую дату в соответствии с требуемым форматом
            print(day)
            print(current_time.strftime("%H:%M"))
            # Обновляем настройки пользователя в базе данных
            update_query = {
                f"statistics.{day}": {
                    'logs': [],
                    'worktime': ''
                }
            }
            staff_collection.update_one({'login': login}, {'$set': update_query})

            access_token = create_access_token(identity=login)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'incorrect password'}), 401


# админа зарегестрировать сотрудника
@app.route('/staff', methods=['POST'])
@jwt_required()
def register_staff():
    if enterprises_collection.find_one({"email": get_jwt_identity()}):
        data = request.form
        name = data.get('name')
        position = data.get('position')
        timetable = json.loads(data.get('timetable'))
        startTime = data.get('startTime')
        endTime = data.get('endTime')

        org_id = enterprises_collection.find_one({"email": get_jwt_identity()})['_id']

        if request.files.get("face") != None:
            image = request.files['face']

            path = os.path.join(app.root_path, 'images', str(org_id))
            if not os.path.exists(path):
                os.makedirs(path)
            path = os.path.join(app.root_path, 'images', str(org_id), name + image.filename)
            image.save(path)

            user_data = {
                'name': name,
                'position': position,
                'statistics': [],
                'timetable': timetable,
                'worktime': {
                    'start': startTime,
                    'end': endTime
                },
                'org_id': ObjectId(org_id),
                'photo_path': path,
            }

            add_to_database(user_data, 'staff')

            with open(path, 'rb') as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                print(base64_image)
                user_data['photo'] = base64_image
            # Send user data to WebSocket server
            staff_ = staff_collection.find_one({'photo_path': user_data['photo_path']})
            user_data['_id'] = str(staff_.get('_id'))

            asyncio.run(send_user_data_to_ws(user_data))

            return jsonify({'message': 'User registered successfully'}), 200

        else:
            return jsonify({'message': 'no photo in request'}), 200


async def send_user_data_to_ws(user_data):
    async with websockets.connect(wsUrl + "/add") as websocket:
        print(user_data, user_data.get('org_id'))
        await websocket.send((json.dumps({'apiId': str(user_data['org_id'])})))
        serialized_result = json.dumps(user_data, default=serialize_object)
        print(serialized_result)
        await websocket.send(serialized_result)


# изменить параметры сотрудника
@app.route('/staff', methods=['PUT'])
@jwt_required()
def update_staff():
    data = request.form
    updated_fields = {}
    # Обновляем только поля, которые были переданы
    for key in data:
        updated_fields[key] = data[key]

    # Удаляем поля, которые не нужно обновлять
    if request.files.get("face") != None:
        image = request.files['face']

        print('avatar::::::::::::::', image)
        path = os.path.join(app.root_path, 'images',
                            enterprises_collection.find_one({"email": get_jwt_identity()})['name'],
                            staff_collection.find_one({"_id": "_id"})['name'],
                            image.filename)
        image.save(path)
        updated_fields.pop('_id', None)
        updated_fields.pop('login', None)
        updated_fields.pop('password', None)
        updated_fields['photo_path'] = path

    staff_collection.update_one({'_id': ObjectId(data.get('id'))}, {'$set': updated_fields})
    return jsonify({'message': 'Staff updated successfully'}), 200


# получить данные о пользователе по id
@app.route('/staff', methods=['GET'])
@jwt_required()
def get_staff():
    email = get_jwt_identity()
    if enterprises_collection.find_one({"email": email}) or staff_collection.find_one({"email": email}):
        data = request.get_json()
        staff = staff_collection.find_one({'_id': ObjectId(data.get('id'))})
        if staff:
            serialized_result = json.loads(json.dumps(staff, default=serialize_object))
            return serialized_result
        else:
            return jsonify({'message': 'Staff not found'}), 404


# все сотрудники
@app.route('/staffs', methods=['GET'])
@jwt_required()
def get_staffs():
    enter = enterprises_collection.find_one({"email": get_jwt_identity()})
    print(enter)
    if enter:
        staffs = staff_collection.find({'org_id': enter["_id"]})
        staff_list = [staff for staff in staffs]
        serialized_result = json.loads(json.dumps(staff_list, default=serialize_object))
        return serialized_result


# данные о предприятии
@app.route('/get_enterprise', methods=['POST'])
@jwt_required()
def get_enterprise():
    if enterprises_collection.find_one(
            {"email": get_jwt_identity()}):
        data = request.get_json()
        enterprise = enterprises_collection.find_one({'_id': ObjectId(data.get('id'))})
        if enterprise:
            serialized_result = json.loads(json.dumps(enterprise, default=serialize_object))
            return serialized_result
        else:
            return jsonify({'message': 'Организация не найдена'}), 404


@app.route('/account', methods=['GET'])
@jwt_required()
def get_account():
    enterprise = enterprises_collection.find_one(
        {"email": get_jwt_identity()})
    if enterprise:
        del enterprise['password']
        serialized_result = json.loads(json.dumps(enterprise, default=serialize_object))
        return serialized_result
    else:
        return jsonify({'message': 'none'}), 404


# добавить предприятие
@app.route('/enterprise', methods=['POST'])
@jwt_required()
def add_enterprise():
    if enterprises_collection.find_one({"email": get_jwt_identity()}):
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
        if not enterprises_collection.find_one({"email": email}):
            add_to_database({"name": name, "email": email, "type": "enterprise",
                             "password": generate_password_hash(password, method='pbkdf2:sha256')}, 'enterprise')
            return jsonify({'message': 'Организация добавлена успешно'}), 200
        else:
            return jsonify({'message': 'организация уже существует'})


# обновить данные предприятия
@app.route('/enterprise', methods=['PUT'])
@jwt_required()
def update_enterprise():
    if enterprises_collection.find_one({"email": get_jwt_identity()}) or enterprises_collection.find_one(
            {"email": get_jwt_identity()}):
        data = request.get_json()
        updated_fields = {}
        for key in data:
            updated_fields[key] = data[key]

        updated_fields.pop('id', None)
        updated_fields['password'] = generate_password_hash('123456', method='pbkdf2:sha256')
        enterprises_collection.update_one({'_id': ObjectId(data.get('id'))}, {'$set': updated_fields})

        return jsonify({'message': 'Enterprise updated successfully'}), 200


# все предприятия
@app.route('/enterprises', methods=['GET'])
@jwt_required()
def get_enterprises():
    enterprise = enterprises_collection.find_one({"email": get_jwt_identity()})
    if enterprise:
        enterprises = enterprises_collection.find({}, {
            "password": 0})  # Используйте проекцию, чтобы исключить поле "password"
        serialized_result = json.loads(json.dumps(list(enterprises), default=serialize_object))
        return serialized_result
    return []


@app.route('/delete', methods=['POST'])
@jwt_required()
def delete_user():
    data = request.get_json()
    user_id = data.get('id')
    user_type = data.get('type')  # Тип пользователя: 'staff' или 'enterprise'

    # Проверяем, является ли пользователь администратором предприятия
    if enterprises_collection.find_one({"email": get_jwt_identity()}):
        if user_type == 'staff':
            result = staff_collection.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count == 1:
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                return jsonify({'message': 'User not found'}), 404
        elif user_type == 'enterprise':
            result = enterprises_collection.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count == 1:
                return jsonify({'message': 'Enterprise deleted successfully'}), 200
            else:
                return jsonify({'message': 'Enterprise not found'}), 404
        else:
            return jsonify({'message': 'Invalid user type'}), 400
    else:
        return jsonify({'message': 'Unauthorized'}), 401


def addAdminUser():
    new_user_data = {
        "email": "admin@admin.admin",
        "name": "admin",
        "type": "admin"
    }

    # Поиск пользователя по email
    existing_user = enterprises_collection.find_one({"email": new_user_data["email"]})

    if not existing_user:
        # Генерация хеша пароля
        hashed_password = generate_password_hash('123456', method='pbkdf2:sha256')
        new_user_data["password"] = hashed_password
        # Добавление пользователя в коллекцию
        enterprises_collection.insert_one(new_user_data)
        print("Пользователь успешно добавлен. Пароль:", '123456')
    else:
        print("Пользователь уже существует в базе данных.")


if __name__ == '__main__':
    addAdminUser()
    app.run(debug=True)
    # http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    # http_server.serve_forever()
