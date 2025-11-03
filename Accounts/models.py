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
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)

class AnonymousUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    full_name = models.TextField()
    contact_number = models.IntegerField()
    email = models.EmailField()
    shipping_address = models.CharField()
    city = models.TextField()
    province = models.CharField()
    postal_code = models.IntegerField()

    class Meta:
        verbose_name = 'anonymous_user'
    def __str__(self):
        return self.email
    

class Cart(models.Model):
 class Payment_Method(models.TextChoices):
       ONLINE = "ONLINE","Online"
       COD = "COD",'Cod'

 class Status(models.TextChoices):
        IN_CART = 'IN_CART', 'In Cart'
        PURCHASED = 'PURCHASED', 'Purchased'
        WISHLIST = 'WISHLIST', 'Wishlist'
 id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
 product  = models.ForeignKey(Saflora_Product,on_delete=models.CASCADE,null=True)
 item = models.ForeignKey(Saflora_Base_Product,null=True,on_delete=models.CASCADE)
 user = models.ForeignKey(Saflora_user, verbose_name="User", on_delete=models.CASCADE,related_name='Saflora_user',null=True)
 anonymous_user = models.ForeignKey(AnonymousUser,null=True,on_delete=models.CASCADE)
 payment_method = models.CharField(choices=Payment_Method.choices,null=True)
 cart_status = models.CharField(choices=Status.choices,default=Status.IN_CART)
 added_at = models.DateTimeField(auto_now_add=True)
 quantity = models.IntegerField(default=0)
 variant = models.CharField(null=True)
 total_price = models.FloatField(null=True)
 paid_price = models.FloatField(null=True)

 def __str__(self):
     user = 'None'
     if self.user:
         user = self.user
     elif self.anonymous_user:
        user = self.anonymous_user.email
     return f"{self.product} in {user} Cart "
 


