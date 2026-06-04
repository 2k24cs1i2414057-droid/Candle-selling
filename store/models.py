from django.db import models
from django.db import models

class Candle(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='candles/')
    category = models.CharField(max_length=100, default="General")

    def __str__(self):
        return self.name


from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )
    candle = models.ForeignKey(
        Candle,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)