from django.db import models

# Create your models here.
class Products(models.Model):
    product_name = models.CharField(max_length=140)
    price = models.IntegerField()
    dimension = models.CharField(max_length=40)
    colours = models.CharField(max_length=200)
    material = models.CharField(max_length=50)
    image = models.CharField(max_length=300)
    seen = models.BooleanField(default=False)

