from django.db import models
import uuid
from Product.models import Saflora_Product
from Accounts.models import Saflora_user

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

    user = models.ForeignKey(Saflora_user,verbose_name=("User"), on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    product = models.ForeignKey(Saflora_Product, verbose_name="Product",on_delete=models.CASCADE,null=True)
    status =models.CharField(choices=Status.choices,verbose_name='Payment Status  ')  
    created_at = models.DateTimeField(auto_now_add=True)

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
       return f"{self.user}`s order of {self.product}"





    