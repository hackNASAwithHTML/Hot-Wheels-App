from django.db import models

# Create your models here.
class DieCastModel(models.Model):
    toy_code = models.CharField(max_length=254, null=True)
    casting_name=models.CharField(max_length=254, null=True)
    series = models.CharField(max_length=254,null=True)
    year = models.CharField(max_length=254,null=True)
    made_in = (
        ("Thaidland", "Thailand"),
        ("Indonesia", "Indonesia"),
        ("Malaysia", "Malaysia"),
        ("China", "China"),
    )
    choice = models.CharField(max_length=20, choices=made_in, default='Thailand')
    color=models.CharField(max_length=254,null=True)
    loose_photo=models.BinaryField()
