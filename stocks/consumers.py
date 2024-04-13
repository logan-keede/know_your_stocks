import json
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from dhanhq import marketfeed
from dhanhq.marketfeed import DhanSDKHelper
import websockets
WSS_URL = 'wss://api-feed.dhan.co'


class Feed(marketfeed.DhanFeed):
    async def connect(self):
        """Initiates the connection to the Websockets"""
        if not self.ws or self.ws.closed:
            self.ws = await websockets.connect(WSS_URL)
            helper = DhanSDKHelper(self)
            await helper.on_connection_established(self.ws)
            await self.authorize()
            await self.subscribe_instruments()

            # Handling incoming messages in a loop to keep the connection open
            # while True:
            for i in range(len(self.instruments)):
                try:
                    response = await self.ws.recv()
                    self.data = self.process_data(response)
                    await helper.on_message_received(self.data)
                except websockets.exceptions.ConnectionClosed:
                    print("Connection has been closed")
                    
class MarketFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # await self.feed.connect()
    async def disconnect(self, close_code):
        print("Connection band ho gaya")
        pass

    async def receive(self, text_data):
        # print(type(text_data))
        text_data= json.loads(text_data)

        instruments = text_data["instruments"]
        client_id = text_data["client_id"]
        access_token = text_data["access_token"]
        
        if text_data["code"]=="Quote":
            subscription_code = marketfeed.Quote
        elif text_data["code"]=="Ticker":
            subscription_code = marketfeed.Ticker 
        else:
            subscription_code = marketfeed.Depth 

        async def on_connect(instance):
            print("Connected to websocket")

        async def on_message(instance, message):
            print(message)
            await self.send(text_data=json.dumps(
                {
                    'type': 'market_data_update',
                    'data': message
                }
            ))


        self.feed = marketfeed.DhanFeed(
            client_id,
            access_token,
            instruments,
            subscription_code,
            on_connect=on_connect,
            on_message=on_message
        )
        await self.feed.connect()
        
        # pass

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    async def disconnect(self, close_code):
        pass
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

class PracticeConsumer(AsyncJsonWebsocketConsumer):
      async def connect(self):
           await self.accept()

      async def receive(self, text_data=None, bytes_data=None, **kwargs):
            if text_data == 'PING':
                 await self.send('PONG')


# const socket = new WebSocket("ws://localhost:8000/live_market_feed/");

#             socket.onopen = function(event) {
#                 const message = { 'client_id' : "Dhan Client ID",
#                 'access_token' : "Access Token", 'instruments' : [[1, "1333"],[0,"13"]],
#                 'code':'Quote'};
#                 socket.send(JSON.stringify(message));
#             };

#             socket.onmessage = function(event) {
#                 const message = JSON.parse(event.data);
#                 console.log("Received:", message);

#                 // Update UI or perform other actions with the received data
#             };
