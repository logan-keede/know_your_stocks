# from django.test import TestCase

# Create your tests here.
from dhanhq import marketfeed
from dhanhq.marketfeed import DhanSDKHelper
import websockets
WSS_URL = 'wss://api-feed.dhan.co'
# Add your Dhan Client ID and Access Token
client_id = "Dhan Client ID"
access_token = "Access Token"

# Structure for subscribing is ("exchange_segment","security_id")

# Maximum 100 instruments can be subscribed, then use 'subscribe_symbols' function 

instruments = [(1, "1333"),(0,"13")]

# Type of data subscription
subscription_code = marketfeed.Quote

# Ticker - Ticker Data
# Quote - Quote Data
# Depth - Market Depth


async def on_connect(instance):
    print("Connected to websocket")

async def on_message(instance, message):
    print("Received:", message)

print("Subscription code :", subscription_code)

class Feed(marketfeed.DhanFeed):
    async def connect(self):
        """Initiates the connection to the Websockets"""
        if not self.ws or self.ws.closed:
            self.ws = await websockets.connect(WSS_URL)
            helper = DhanSDKHelper(self)
            await helper.on_connection_established(self.ws)
            await self.authorize()
            await self.subscribe_instruments()

            for i in range(len(self.instruments)):
                try:
                    response = await self.ws.recv()
                    self.data = self.process_data(response)
                    await helper.on_message_received(self.data)
                except websockets.exceptions.ConnectionClosed:
                    print("Connection has been closed")



feed = Feed(client_id,
    access_token,
    instruments,
    subscription_code,
    on_connect=on_connect,
    on_message=on_message)
feed.run_forever()


