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
    class Fragnence(models.TextChoices):
        LEMON = 'LEMON','lemon'
        JASMINE = 'JASMIE','Jasmine'

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
    fragnence = models.CharField(choices=Fragnence.choices,null=True)
    class Meta():
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('-created',)
    def __str__(self):
        return self.name
    

class Saflora_Base_Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    item_name = models.CharField(verbose_name="item_name")
    item_image = models.ImageField(upload_to='item_image')
    item_description = models.TextField()
    items_variants = models.ManyToManyField(Saflora_Product)
    price = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.item_name}"
    
    class Meta:
        verbose_name = "Saflora item"