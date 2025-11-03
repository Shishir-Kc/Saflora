from django.db import models
import uuid
from Product.models import Saflora_Product
from Accounts.models import Saflora_user,AnonymousUser,Cart
from datetime import timedelta,datetime
from django.utils import timezone

def expires_at():
   return timezone.now() + timedelta(minutes=1)

class Payment_Records(models.Model):
    class Status(models.TextChoices):
      COMPLETED = "COMPLETED","Completed"
      PENDING = "PENDING","Pending"
      EXPIRED = "EXPIRED",'Expired'
      INITIATED = "INITIATED","Initiated"
      REFUNDED = "REFUNDED","Refunded"
      USER_CANCLED = "USER_CANCLED","User canceled"
      PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED","Partially Refunded"
      FAILED = "FAILED","Failed"
    class Payment_Provider(models.TextChoices):
       KHALTI = "KHALTI","Khalti"
       ESEWA = "ESEWA","Esewa"
    class Payment_Method(models.TextChoices):
       ONLINE = "ONLINE","Online"
       COD = "COD",'Cod'


    user = models.ForeignKey(Saflora_user,verbose_name=("User"), on_delete=models.CASCADE,null=True)
    anonymous_user = models.ForeignKey(AnonymousUser,null=True,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    product = models.ForeignKey(Saflora_Product, verbose_name="Product",on_delete=models.CASCADE,null=True)
    status =models.CharField(choices=Status.choices,verbose_name='Payment Status  ')  
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(choices=Payment_Method.choices,null=True)
    payment_session = models.DateTimeField(default=expires_at)
   #cart
    cart = models.ForeignKey(Cart, verbose_name=("Cart"), on_delete=models.CASCADE,null=True) 


    # service porviders 

    provider = models.CharField(choices=Payment_Provider.choices,verbose_name="Payment_Provider")
    pidx = models.CharField(verbose_name="PIDX",editable=False,max_length=255)
    total_amount = models.FloatField()
    transaction_id = models.CharField(max_length=255,editable=False)
    service_provider_status = models.CharField(choices=Status.choices,verbose_name="Service Provider Status")
    fee = models.FloatField(blank=True,null=True)
    refunded = models.BooleanField(default=False)


    class Meta:
       verbose_name = "Payment Record"


    def __str__(self):
       if self.user:
          user = self.user
       elif self.anonymous_user:
         user = self.anonymous_user.email
       return f"{user}`s order of {self.product}"





    