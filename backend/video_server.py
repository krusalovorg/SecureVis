import asyncio
import json
import websockets
from websockets import WebSocketServerProtocol

connected = {}  # Словарь для хранения айди клиентов и соответствующих веб-сокетов
connected_id = {}

async def handle_connect(websocket):
    # Запросите у клиента учетные данные
    packet = await websocket.recv()
    # Проверьте учетные данные на сервере
    print('get packet', packet)
    data = json.loads(packet)
    api_id = data.get("apiId")
    if api_id not in connected:
        connected[api_id] = []  # Создаем пустой список для айди, если его еще нет
    connected[api_id].append(websocket)  # Добавляем веб-сокет в список по айди
    connected_id[websocket.id] = api_id
    print(f"Client connected with API ID: {api_id}")
    print(connected)


async def video_receiver(websocket: WebSocketServerProtocol, path):
    global connected
    print(websocket, path)

    await handle_connect(websocket)

    if path == '/add':
        pass  # Дополнительная логика для обработки других путей

    if path == '/video':
        try:
            async for video in websocket:
                for ws in connected.get(connected_id.get(websocket.id), []):
                    if ws != websocket:
                        try:
                            await asyncio.wait_for(ws.send(video), timeout=1)
                        except Exception as e:
                            print(f"Error sending video to client: {e}")
        finally:
            print('Клиент отключен')
            # Удаляем закрытых клиентов из списка
            # connected[api_id] = [ws for ws in connected.get(api_id, []) if not ws.closed]

    async for packet in websocket:
        print(packet)

start_server = websockets.serve(video_receiver, '127.0.0.1', 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
