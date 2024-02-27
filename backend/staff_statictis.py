import time
import pygetwindow as gw
import requests


def send_data_to_server(apps, id):
    url = "http://127.0.0.1:5000/staff_apps"  # Замените на адрес вашего сервера
    data = {}
    data['apps'] = apps
    data['id'] = id
    print(data)
    # Отправляем данные на сервер
    requests.post(url, json=data)


# Словарь для хранения времени использования каждого приложения
apps_usage = {}


def record_usage(app_name, start_time):
    """
    Записывает время использования приложения в словарь apps_usage.
    """
    if app_name in apps_usage:
        # Если приложение уже есть в словаре, обновляем его время использования
        apps_usage[app_name] += round(time.time() - start_time)
    else:
        # Если приложение новое, добавляем его в словарь
        apps_usage[app_name] = round(time.time() - start_time)


# Основной цикл программы
active_app = None
people_id = input("Введите ваш id: ")
start_time = time.time()
while True:
    current_active_window = gw.getActiveWindow()
    if current_active_window is not None:
        # Получаем название активного окна
        new_app = current_active_window.title

        # Проверяем, отличается ли активное окно от предыдущего
        if new_app != active_app:
            # Если да, записываем время использования предыдущего приложения
            if active_app is not None:
                if ' - ' in active_app:
                    active_app = active_app.split(' - ')[1]
                elif ' – ' in active_app:
                    active_app = active_app.split(' – ')[1]
                record_usage(active_app, start_time)

            # Обновляем активное окно и время начала использования
            active_app = new_app
            start_time = time.time()
            print(apps_usage)
            send_data_to_server(apps_usage, people_id)

    # Ждем некоторое время перед следующей проверкой
    time.sleep(1)

    # Выход из цикла по вводу 'exit'
    if active_app == 'exit':
        break

# Записываем время использования последнего приложения перед выходом
if active_app is not None:
    record_usage(active_app, start_time)
