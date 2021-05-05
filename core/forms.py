from django import forms

class PayForm(forms.Form):
    coin_amount = forms.IntegerField()
 