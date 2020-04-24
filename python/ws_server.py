
import asyncio
import websockets
from websockets import WebSocketServerProtocol

import threading
import time

class weServer:
    clients = set()
    
    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        print(f'{ws.remote_address} connects')
    
    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        print(f'{ws.remote_address} disconnects')
        
    async def send_clients(self, msg: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(msg) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)
        
    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for msg in ws:
            await self.send_clients(msg)

def init_server(loop):  
    asyncio.set_event_loop(loop)
    server = weServer()
    start_server = websockets.serve(server.ws_handler, 'localhost', 4000)
    loop.run_until_complete(start_server)
    loop.run_forever()

loop = asyncio.new_event_loop()
t = threading.Thread(target=init_server, args=(loop,))
t.start()

while(True):
    print('Aqui sigo')
    time.sleep(10)
    
print("Finish")
    