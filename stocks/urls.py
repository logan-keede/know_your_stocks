from django.urls import path, include
from .views import *

urlpatterns = [
    path('get_holdings/', get_holdings, name='get_holdings'),
    path('place_buy_order/', place_buy_order, name='place_buy_order'),
    path('get_order_list/', get_order_list, name='get_order_list'),
    path('get_trade_book/', get_trade_book, name='get_trade_book'),
    path('cancel_order/', cancel_order, name='cancel_order'),
    path('fill_form/', fill_form, name='fill_form'),
    path('postback/<int:id>/', postback, name="postback")
    # path('live_feed/', live_feed, name='live_feed'),
    # Add more paths for other views if needed
]