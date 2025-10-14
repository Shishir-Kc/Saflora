from django.db import models
import random


class Verification_code(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"
        ordering = ['-created_at']

    @classmethod
    def generate_code(cls,email):
        number = [0,1,2,3,4,5,6,7,8,9]
        alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

        code = str(random.choice(number)) + str(random.choice(number)) + str(random.choice(number)) + str(random.choice(alphabets)) + str(random.choice(alphabets)) + str(random.choice(alphabets))
        return cls.objects.create(email=email, code=code)

    def __str__(self):
        return f"Verification code for {self.email}"