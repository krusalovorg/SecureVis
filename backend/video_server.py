import asyncio
import websockets
from websockets import WebSocketServerProtocol

connected = []  # Используем список вместо множества

async def video_receiver(websocket: WebSocketServerProtocol, path):
    global connected
    print(websocket, path)

    connected.append(websocket)  # Добавляем клиента в список

    try:
        async for video in websocket:
            print(video[0:100])
            for ws in connected:
                print('send', ws.path)
                if ws != websocket:
                    try:
                        await asyncio.wait_for(ws.send(video), timeout=1)
                    except Exception as e:
                        print(e)
                    finally:
                        pass
    finally:
        print('отключено')
        # Удаляем закрытых клиентов из списка
        connected = [ws for ws in connected if not ws.closed]

start_server = websockets.serve(video_receiver, '127.0.0.1', 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()