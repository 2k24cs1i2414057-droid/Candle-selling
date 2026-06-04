from django.shortcuts import render
from .models import Candle
import json

def products(request):
    candles = Candle.objects.all()

    products_data = []

    for candle in candles:
        products_data.append({
            "id": candle.id,
            "name": candle.name,
            "sub": candle.category,
            "type": candle.category,
            "img": candle.image.url if candle.image else "",
            "price": float(candle.price),
            "desc": candle.description,
            "badge": "New",
            "badgeClass": "new-badge"
        })

    return render(
        request,
        "home/candle.html",
        {
            "products_json": json.dumps(products_data)
        }
    )

from django.http import JsonResponse
from .models import Candle, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):

    candle = Candle.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(id=1)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        candle=candle
    )

    if not created:
        item.quantity += 1
        item.save()

    count = sum(
        item.quantity
        for item in CartItem.objects.filter(cart=cart)
    )

    return JsonResponse({
        "success": True,
        "count": count
    })

from django.http import JsonResponse
from .models import CartItem

def clear_cart(request):
    CartItem.objects.all().delete()
    return JsonResponse({"success": True})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_cart(request):

    cart, created = Cart.objects.get_or_create(id=1)

    items = []

    for item in CartItem.objects.filter(cart=cart):

        items.append({
            "id": item.candle.id,
            "name": item.candle.name,
            "price": float(item.candle.price),
            "img": item.candle.image.url,
            "qty": item.quantity,
        })

    return JsonResponse({
        "items": items
    })

from .models import Cart, CartItem

def remove_from_cart(request, product_id):
    cart = Cart.objects.get(id=1)

    CartItem.objects.filter(
        cart=cart,
        candle_id=product_id
    ).delete()

    return JsonResponse({
        "success": True
    })

    return JsonResponse({"success": True})