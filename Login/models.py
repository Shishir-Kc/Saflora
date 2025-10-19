from django.db import models
import random
from datetime import timedelta
from django.utils import timezone



def default_expiry():
    return timezone.now() + timedelta(minutes=5)

class Verification_code(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(default= default_expiry())

    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"
        ordering = ['-created_at']

    @classmethod
    def generate_code(cls,email):
        now= timezone.now()
        number = [0,1,2,3,4,5,6,7,8,9]
        alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

        code = str(random.choice(number)) + str(random.choice(number)) + str(random.choice(number)) + str(random.choice(alphabets)) + str(random.choice(alphabets)) + str(random.choice(alphabets))
        expires_at = now +timedelta(minutes=5)   
        return cls.objects.create(email=email, code=code,expires_at=expires_at)
    
    def __str__(self):
        return f"Verification code for {self.email}"