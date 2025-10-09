from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Saflora_user(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    contact = models.IntegerField(null=True, blank=True)



# need to dd {where did u hear about us?} field later
