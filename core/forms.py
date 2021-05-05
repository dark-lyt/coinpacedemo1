from django import forms
from django.forms.fields import IntegerField

class PayForm(forms.Form):
    coin_amount = forms.IntegerField()
 

class ContactForm(forms.Form):
    pass

class WithdrawForm(forms.Form):
    amount = forms.IntegerField()
    address = forms.Textarea()
