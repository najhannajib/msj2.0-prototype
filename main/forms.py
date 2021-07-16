from django import forms

from django.forms import fields
from .models import health, vaccine, location_qr, post2
from main import models
# from .models import profile

class healthupdateform(forms.ModelForm):
    class Meta:
        model = health
        fields = [
            'fever',
            'chills', 
            'headache', 
            'vomiting',
            'diarrhea',
            ] 

class DateInput(forms.DateInput):
    input_type = 'date'

class post2form(forms.ModelForm):
    class Meta:
        model = post2
        fields = [
            'date',
            'new',
            'cured',
            'totalcases',
            'newdeath',
            'totaldeath'
        ]
        widgets = {
            'date': DateInput(),
        }


class vaccineform(forms.ModelForm):
    class Meta:
        model = vaccine
        fields = [
            'name',
            'age',
            'state',
            'date'
        ]
        widgets = {
            'date': DateInput(),
        }

class qrcreateform(forms.ModelForm):
    class Meta:
        model = location_qr
        fields = [
            'name', 'address', 'city', 'state'
        ]
