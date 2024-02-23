import base64
import threading

import cv2
from backend.modules.face import loadFaces, detect_faces_in_video
import socketio

sio = socketio.Client()
connected = False

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('message', 'Hello, Server!')

@sio.event
def response(data):
    print('Response from server: ', data)

# @sio.event
# def connect():
#     global connected
#     print("I'm connected!")
#     connected = True
#     sio.emit('frame', {'image': 'encoded_image'})
@sio.event
def connect_error():
    global connected
    print("The connection failed!")
    connected = False

@sio.event
def disconnect():
    print("I'm disconnected!")

def send_frame_to_server(frame):
    global connected
    print('encoded_image',connected)

    if not connected:
        return
    retval, buffer = cv2.imencode('.jpg', frame)
    encoded_image = base64.b64encode(buffer).decode()
    sio.emit('frame', {'image': 'encoded_image'})

userIds = ["Egor"]
loadFaces(userIds[0])

if __name__ == '__main__':
    # Создайте поток, указав вашу функцию в качестве цели
    #thread = threading.Thread(target=detect_faces_in_video, args=(userIds, send_frame_to_server))
    # Запустите поток
    #thread.start()

    sio.connect('http://127.0.0.1:5000', wait_timeout=10)
    sio.emit('test', {'tset': 'tset'})
    sio.wait()