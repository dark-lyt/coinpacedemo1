from django.shortcuts import render
from cryptocurrency_payment.models import create_new_payment
from django.conf import settings



def home(request):
    # print(request.user.profile)
    # payment = create_new_payment(crypto='BITCOIN', #Cryptocurrency from your backend settings
    #             fiat_amount=20, #Amount of actual item in fiat
    #             fiat_currency='USD', #Fiat currency used to convert to crypto amount
    #             payment_title="NG",  #Title associated with payment
    #             payment_description="TING1", #Description associated with payment
    #             related_object=None, #Generic linked object for this payment -> crypto_payments = GenericRelation(CryptoCurrencyPayment)
    #             user=None, #User of this payment for non-anonymous payment
    #             parent_payment=None, #Obvious
    #             address_index=None,# Use a particular address index for this payment
    #             reuse_address=None) #Used previously paid address for this payment  
    # print(payment.address)
    # payment.save()
    # print(payment)
    return render(request, "core/index.html")

def about(request):
    return render(request, "core/about.html")

def services(request):
    return render(request, "core/services.html")

def price(request):
    return render(request, "core/price.html")

def terms(request):
    return render(request, "core/terms.html")

def contact(request):
    return render(request, "core/contact.html")

