import asyncio
import cv2
import base64

import face_recognition
import websockets

from backend.modules.face import loadFacesModels


async def detect_faces_in_video(userIds):
    # Загрузите изображение и получите его кодировку
    face_encodings = loadFacesModels(userIds)

    # Получите видеопоток с веб-камеры
    video_capture = cv2.VideoCapture(0)

    while True:
        # Захватите один кадр видео
        ret, frame = video_capture.read()

        # Найдите все лица на кадре и их кодировки
        face_locations = face_recognition.face_locations(frame)
        unknown_face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in unknown_face_encodings:
            # Проверяем, есть ли лица на изображении
            if len(face_encoding) > 0:
                name = "Unknown"
                # Сравните известные кодировки лиц с кодировкой неизвестного лица
                for userId, known_face_encodings in face_encodings.items():
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    # Если есть совпадение, используем первое совпадение
                    if True in matches:
                        name = userId
                        break

                # Рисуем прямоугольник вокруг лица и подписываем его именем
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)


        # Показываем результат
        cv2.imshow('Video', frame)

        # Если пользователь нажал 'q', выйдите из цикла

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        _, buffer = cv2.imencode('.jpg', frame)
        video = base64.b64encode(buffer).decode()
        await asyncio.sleep(0.5)
        yield video

    # Освободите ресурсы и закройте окна
    video_capture.release()
    cv2.destroyAllWindows()


async def video_sender(uri):
    global websocket_client
    async with websockets.connect(uri) as websocket:
        async for video in detect_faces_in_video(userIds):
            await websocket.send(video)


userIds = ["Egor"]

asyncio.run(video_sender('ws://127.0.0.1:5001/video'))