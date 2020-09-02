from django.db import models

# Create your models here.
class Seller(models.Model):
    profile=models.BinaryField(null=True)
    seller_name = models.CharField(max_length=254, null=True)
    location=models.CharField(max_length=254, null=True)
    product_name = models.CharField(max_length=254, null=True)
    price = models.CharField(max_length=254,null=True)
    token = models.CharField(max_length=254,null=True)
    status = models.CharField(max_length=254,null=True)
    image=models.BinaryField()
