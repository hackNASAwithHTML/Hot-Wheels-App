from django import forms as Fform
from .models import  Seller
class SellerForm(Fform.ModelForm):
    class Meta:
        model=Seller
        fields=[
            'seller_name','location','product_name','price','token',
            'status'
        ]