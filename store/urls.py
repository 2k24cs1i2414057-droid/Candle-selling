from django.urls import path
from .views import (
    products,
    add_to_cart,
    clear_cart,
    get_cart,
    remove_from_cart
)


urlpatterns = [
    path('', products, name='products'),
    
]
from django.urls import path
from .views import products, add_to_cart


urlpatterns = [
    path('', products, name='products'),

    path(
        'add-to-cart/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('get-cart/', get_cart, name='get_cart'),
    path(
    'remove-from-cart/<int:product_id>/',
    remove_from_cart,
    name='remove_from_cart'
),
]