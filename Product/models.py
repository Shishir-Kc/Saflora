from django.db import models
import uuid

class Feature(models.Model):
    name  = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Variants(models.Model):
    variant = models.CharField()
    class Meta:
        verbose_name = "variant"
    def __str__(self):
        return self.variant

class Saflora_Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    variant = models.ManyToManyField(Variants)
    class Meta():
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('-created',)
    def __str__(self):
        return self.name
    

