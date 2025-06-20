# your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import get_current_player_info
import asyncio

class BiddingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("HELLO")
        await self.accept()
        while True:
            data = get_current_player_info()
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        self.keep_sending = False

    async def send_updates(self):
        while self.keep_sending:
            player_info = get_current_player_info()
            await self.send(text_data=json.dumps(player_info))
            await asyncio.sleep(1)
