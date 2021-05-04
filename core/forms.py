from django import forms

class PayForm(forms.Form):
    toPay = forms.IntegerField()
 