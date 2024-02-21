import os
import pickle
import face_recognition
import cv2
import numpy as np


def loadFaces(userId):
    # Укажите путь к папке с обучающими изображениями
    training_folder = f"../userdata/{userId}"
    encodings_file = f"../userdata/{userId}/model.pkl"

    if os.path.exists(encodings_file):
        # Если файл существует, загружаем кодировки
        with open(encodings_file, 'rb') as f:
            face_encodings = pickle.load(f)
        print("Model is loaded")
    else:
        # Если файла нет, загружаем изображения для обучения и получаем кодировки лиц
        image_files = os.listdir(training_folder)
        face_encodings = []
        for image_file in image_files:
            image = face_recognition.load_image_file(os.path.join(training_folder, image_file))
            encodings = face_recognition.face_encodings(image)
            if encodings:
                face_encodings.append(encodings[0])

        # Проверяем, существует ли папка для сохранения файла
        if not os.path.exists(training_folder):
            os.makedirs(training_folder)

        # Сохраняем кодировки в файл
        with open(encodings_file, 'wb') as f:
            pickle.dump(face_encodings, f)
        print("Model saved")
    return face_encodings

# Функция для поиска лица на фото
def find_face(image_recognition, userId=""):
    # Загрузите изображение и получите его кодировку
    face_encodings = loadFaces(userId)
    unknown_image = face_recognition.load_image_file(image_recognition)
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)

    if unknown_face_encoding:
        unknown_face_encoding = unknown_face_encoding[0]
    else:
        return False

    # Сравните известные кодировки лиц с кодировкой неизвестного лица
    results = face_recognition.compare_faces(face_encodings, unknown_face_encoding)

    # Если результат содержит True, то лицо найдено
    return True in results

def loadFacesModels(userIds):
    face_encodings = {}
    for userId in userIds:
        # Укажите путь к папке с обучающими изображениями
        training_folder = f"../userdata/{userId}"
        encodings_file = f"../userdata/{userId}/model.pkl"

        if os.path.exists(encodings_file):
            # Если файл существует, загружаем кодировки
            with open(encodings_file, 'rb') as f:
                face_encodings[userId] = pickle.load(f)
    return face_encodings

def detect_faces_in_video(userIds):
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

    # Освободите ресурсы и закройте окна
    video_capture.release()
    cv2.destroyAllWindows()

# Список пользователей, для которых загружаются модели
userIds = ["Egor"]
loadFaces(userIds[0])
detect_faces_in_video(userIds)