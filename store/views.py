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

    cart, created = Cart.objects.get_or_create( user=request.user)

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
@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    return JsonResponse({"success": True})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_cart(request):

    cart, created = Cart.objects.get_or_create( user=request.user)

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
from django.contrib.auth.decorators import login_required
@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)

    CartItem.objects.filter(
        cart=cart,
        candle_id=product_id
    ).delete()

    return JsonResponse({
        "success": True
    })

    return JsonResponse({"success": True})



from .models import Order, OrderItem

@login_required
def checkout(request):

    

    cart = Cart.objects.get(user=request.user)

    order = Order.objects.create(
        user=request.user
    )

    total = 0

    for item in CartItem.objects.filter(cart=cart):

        OrderItem.objects.create(
            order=order,
            candle=item.candle,
            quantity=item.quantity
        )

        total += item.candle.price * item.quantity

    order.total_price = total
    order.save()

    CartItem.objects.filter(cart=cart).delete()

    return JsonResponse({
        "success": True,
        "order_id": order.id
    })


# @login_required
# def my_orders(request):


from .models import Order
from django.db.models import Sum

@login_required
def orders(request):

    user_orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_spent = (
        user_orders.aggregate(
            Sum('total_price')
        )['total_price__sum']
        or 0
    )

    return render(
        request,
        'home/orders.html',
        {
            'orders': user_orders,
            'total_spent': total_spent
        }
    )