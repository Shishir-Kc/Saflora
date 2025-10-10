from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from Product.models import Saflora_Product


class Cart(models.Model):
 class Status(models.TextChoices):
        IN_CART = 'in_cart', 'In Cart'
        PURCHASED = 'purchased', 'Purchased'
        WISHLIST = 'wishlist', 'Wishlist'

 product  = models.ForeignKey(Saflora_Product,on_delete=models.CASCADE)

 def __str__(self):
     return self.product.name

class Saflora_user(AbstractUser):
    class Heard_from(models.TextChoices):
        FRIEND = 'friend', 'Friend'
        SOCIAL_MEDIA = 'social_media', 'Social Media'
        ADVERTISEMENT = 'advertisement', 'Advertisement'
        OTHER = 'other', 'Other'

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    contact = models.IntegerField(null=True, blank=True)
    cart = models.ManyToManyField(Cart, blank=True)
    address = models.TextField(null=True, blank=True)
    hear_about_us = models.CharField(max_length=20,choices=Heard_from.choices,default=Heard_from.OTHER) 


