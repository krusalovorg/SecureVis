import asyncio
import http
import io
import json
import os
import time

import cv2
import base64

import face_recognition
import requests
import websockets
from PIL import Image
import aiohttp
from threading import Thread

from backend.modules.face import loadFaces

face_encodings = []

async def post_request(url, data, image=None):
    headers = {'Content-type': 'application/json'}
    if image is not None:
        # Кодируем изображение в base64 и добавляем его в данные
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        data['image'] = img_str.decode('utf-8')

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data), headers=headers) as response:
            return response.status, await response.text()

class ThreadedCamera(object):
    def __init__(self, source=0):
        self.capture = cv2.VideoCapture(source)
        self.FPS = 1 / 78
        self.source = source
        self.FPS_MS = int(self.FPS * 1000)

        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.frame = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                if not self.status:
                    self.capture.release()
                    self.capture = cv2.VideoCapture(self.source)
                time.sleep(self.FPS)

    def release(self):
        self.capture.release()

    def grab_frame(self):
        if self.status:
            return self.frame
        return None

async def detect_faces_in_video():
    global face_encodings
    # Загрузите изображение и получите его кодировку
    face_encodings = loadFaces()
    last_detection_times = {}
    detection_interval = 25  # время в секундах

    face_encodings_list = []
    for value in face_encodings.values():
        face_encodings_list.extend(value)

    names = list(face_encodings.keys())
    print(names)

    streamer = ThreadedCamera(0)

    while True:
        frame = streamer.grab_frame()

        if frame is None:
            print("Не удалось получить кадр из видеопотока")
            continue

        # Найдите все лица на кадре и их кодировки
        face_locations = face_recognition.face_locations(frame, model="hog")
        unknown_face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, unknown_face_encodings):
            print('face_encoding',face_encoding, len(unknown_face_encodings))
            matches = face_recognition.compare_faces(face_encodings_list, face_encoding)

            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = names[first_match_index]
                print('Найден:', name)
                if name != "Unknown" and (not last_detection_times.get(name, False) or time.time() - last_detection_times.get(name, 0) > detection_interval):
                    last_detection_times[name] = time.time()
                    url = "http://127.0.0.1:5000/user_event"
                    top, right, bottom, left = face_locations[0]
                    face_image = frame[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)
                    # Отправляем изображение на сервер
                    data = {'id': name.split(".")[0]}
                    print(data, name)
                    try:
                        task = asyncio.create_task(post_request(url, data, image=pil_image))
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    break
                else:
                    # Если лицо обнаружено, но не прошло 2 секунды с момента последнего обнаружения, обновляем таймер
                    last_detection_times[name] = time.time()

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # Если пользователь нажал 'q', выйдите из цикла
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        _, buffer = cv2.imencode('.jpg', frame)
        video = base64.b64encode(buffer).decode()
        #await asyncio.sleep(0.5)
        yield video
        #yield '#'

    # Освободите ресурсы и закройте окна
    streamer.release()
    cv2.destroyAllWindows()


async def video_sender(apiId, uri):
    global websocket_client

    async with websockets.connect(uri + "/video") as websocket:
        await websocket.send(json.dumps({
            'apiId': apiId
        }))

        # Создаем задачи для отправки и получения видео
        send_video_task = asyncio.create_task(send_video(websocket))
        receive_video_task = asyncio.create_task(receive_video(websocket))

        # Запускаем задачи параллельно
        await asyncio.gather(send_video_task, receive_video_task)

async def send_video(websocket):
    async for video in detect_faces_in_video():
         await websocket.send(video)

async def receive_video(websocket):
    print('start recive')
    global face_encodings
    async for message in websocket:
        # Обрабатываем полученное видео
        print('get',message)
        userdata = json.loads(message)
        if userdata.get("name"):
            dir_path = f"./userdata"
            os.makedirs(dir_path, exist_ok=True)

            # Получаем расширение файла из photo_path
            _, file_extension = os.path.splitext(userdata.get('photo_path'))

            # Сохраняем файл в папку
            print(userdata.get('_id'),file_extension)
            file_path = f"{dir_path}/{userdata.get('_id')}{file_extension}"
            print('dir path', file_path)
            with open(file_path, 'wb') as f:
                photo_data = base64.b64decode(userdata.get('photo'))
                f.write(photo_data)

            face_encodings = loadFaces()

if __name__ == '__main__':
    apiId = "65d9aa434419fb3469da9ce5"
    wsUrl = 'ws://127.0.0.1:5001'

    asyncio.run(video_sender(apiId, wsUrl))