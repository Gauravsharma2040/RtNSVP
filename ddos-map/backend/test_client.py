import asyncio
import websockets
import json

async def listen():
    uri = "ws://127.0.0.1:8000/ws/traffic"
    try:
        async with websockets.connect(uri) as ws:
            async for msg in ws:
                print(json.loads(msg))
    except websockets.exceptions.ConnectionClosed:
        print("Stream ended.")

asyncio.run(listen())
