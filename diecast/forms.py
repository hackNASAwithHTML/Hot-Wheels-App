from django import forms as Fform
from .models import  DieCastModel
class DieCastForm(Fform.ModelForm):
    class Meta:
        model=DieCastModel
        fields=[
            'toy_code','casting_name','series','year','choice',
            'color'
        ]