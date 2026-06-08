from django.contrib import admin
from .models import Candle, Cart, CartItem, Order, OrderItem

admin.site.register(Candle)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)