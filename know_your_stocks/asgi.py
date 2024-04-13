"""
ASGI config for know_your_stocks project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from stocks.consumers import MarketFeedConsumer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "know_your_stocks.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
         path('live_market_feed/', MarketFeedConsumer.as_asgi())    
        ])
})
print(application)
