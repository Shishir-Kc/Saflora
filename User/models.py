from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from Product.models import Product


class Cart(models.Model):
 class Status(models.TextChoices):
        IN_CART = 'in_cart', 'In Cart'
        PURCHASED = 'purchased', 'Purchased'
        WISHLIST = 'wishlist', 'Wishlist'

 product  = models.ForeignKey(Product,on_delete=models.CASCADE)

 def __str__(self):
     return self.product.name

class Saflora_user(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    contact = models.IntegerField(null=True, blank=True)
    cart = models.ManyToManyField(Cart, blank=True)




# need to dd {where did u hear about us?} field later
