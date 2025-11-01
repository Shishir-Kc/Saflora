from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from Product.models import Saflora_Product,Saflora_Base_Product

class Location(models.Model):
    name = models.TextField(default='itahari')
    class Meta:
        verbose_name  = "location"

    def __str__(self):
        return self.name
    

class Saflora_user(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    contact = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    address_type = models.TextField(null=True)
    hear_about_us = models.CharField(max_length=20,default='Others')
    location = models.OneToOneField(Location,on_delete=models.CASCADE,null=True)


class Cart(models.Model):
 class Status(models.TextChoices):
        IN_CART = 'IN_CART', 'In Cart'
        PURCHASED = 'PURCHASED', 'Purchased'
        WISHLIST = 'WISHLIST', 'Wishlist'
 id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
 product  = models.ForeignKey(Saflora_Product,on_delete=models.CASCADE,null=True)
 item = models.ForeignKey(Saflora_Base_Product,null=True,on_delete=models.CASCADE)
 user = models.ForeignKey(Saflora_user, verbose_name="User", on_delete=models.CASCADE,related_name='Saflora_user',null=True)
 cart_status = models.CharField(choices=Status.choices,default=Status.IN_CART)
 added_at = models.DateTimeField(auto_now_add=True)
 quantity = models.IntegerField(default=0)
 variant = models.CharField(null=True)
 total_price = models.FloatField(null=True)
 paid_price = models.FloatField(null=True)
 def __str__(self):
     return f"{self.product} in {self.user}`s Cart "
 


