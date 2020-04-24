
import asyncio
import websockets

import time

class weClient:
    def __init__(self, ip, port):
        try:
            self.connection = websockets.connect(f"ws://{ip}:{port}")
        except Exception as e:
            raise e
        
    async def send(self, msg):
        async with self.connection as ws:
            await ws.send(msg)
            return await ws.recv()
    
client = weClient("localhost", 4000)
print(asyncio.get_event_loop().run_until_complete(client.send("HORSELUIS")))

print(asyncio.get_event_loop().run_until_complete(client.send("PEPE")))

while(True):
    print('Aqui sigo')
    time.sleep(10)
    
print("Finish")
        