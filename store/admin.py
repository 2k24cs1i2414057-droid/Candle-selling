from django.contrib import admin
from .models import Candle, Cart, CartItem

admin.site.register(Candle)
admin.site.register(Cart)
admin.site.register(CartItem)