from django import forms
from django.forms.fields import IntegerField

class PayForm(forms.Form):
    coin_amount = forms.IntegerField()
 

class ContactForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'id':"firstname",
        'class':"form-control",
        'name':'firstname',
        'placeholder':"FIRST NAME",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'id':"lastname",
        'class':"form-control ",
        'name':'lastname',
        'placeholder':"LAST NAME",
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'id':"subject",
        'class':"form-control ",
        'name':'subject',
        'placeholder':"SUBJECT",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id':"email",
        'name':'email',
        'class':"form-control",
        'placeholder':"EMAIL",
    }))

    snd_message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5,
        'name':'message',
        'id':'message',
        'class':"form-control",
        'placeholder':"MESSAGE",
    }))

class WithdrawForm(forms.Form):
    amount = forms.IntegerField()
    address = forms.Textarea()
