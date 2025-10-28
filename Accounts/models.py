from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from Product.models import Saflora_Product

class Saflora_user(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    contact = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    hear_about_us = models.CharField(max_length=20,default='Others')


class Cart(models.Model):
 class Status(models.TextChoices):
        IN_CART = 'IN_CART', 'In Cart'
        PURCHASED = 'PURCHASED', 'Purchased'
        WISHLIST = 'WISHLIST', 'Wishlist'
 id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
 product  = models.ForeignKey(Saflora_Product,on_delete=models.CASCADE)
 user = models.ForeignKey(Saflora_user, verbose_name="User", on_delete=models.CASCADE,related_name='Saflora_user',null=True)
 cart_status = models.CharField(choices=Status.choices,default=Status.IN_CART)
 added_at = models.DateTimeField(auto_now_add=True)

 def __str__(self):
     return f"{self.product} in {self.user.username}`s Cart "

