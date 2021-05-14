from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect, reverse
import random
from django.contrib.auth.decorators import login_required
import string
from .forms import ContactForm, PayForm
from .models import Item, Order, OrderItem
# from django.views.generic import DetailView,
from cryptocurrency_payment.models import create_new_payment
from django.conf import settings
from coinpace.settings import EMAIL_HOST_USER
from django.core.mail import message, send_mail

ADMIN_MAIL = 'amoakbeall@fuwari.be'


def home(request):
    item_list = Item.objects.all()
    return render(request, "core/index.html", {'item_list':item_list})


def product(request, slug):
    item_list = Item.objects.all()
    item = get_object_or_404(Item, slug=slug)
    form = PayForm(request.POST or None)
    if request.method == "POST":
        print("\nIt got here!!!!\n")
        if form.is_valid():
            print("\nIt got here!!!! and here too\n")
            cd = form.cleaned_data
            price = cd['coin_amount']
            print(price)
            if price >= item.min_price and price <= item.max_price:
                item.to_pay = price
                item.save()
                print(item)
                return redirect('core:add-to-cart', slug=slug)
            else:
                print("ERROR SOMEWHARE")
                messages.info(request, "Please enter a value with the range")
        else:
            print("ERROR SOMEWHARE")
            messages.info(request, "Please enter a value with the range")
    return render(request, 'core/transaction2.html', {'form': form, 'item':item, 'item_list':item_list})    


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    payment = create_new_payment(crypto='BITCOIN', #Cryptocurrency from your backend settings
                fiat_amount=item.to_pay, #Amount of actual item in fiat
                fiat_currency='USD', #Fiat currency used to convert to crypto amount
                payment_title=item.title,  #Title associated with payment
                payment_description=item.label, #Description associated with payment
                related_object=None, #Generic linked object for this payment -> crypto_payments = GenericRelation(CryptoCurrencyPayment)
                user=request.user, #User of this payment for non-anonymous payment
                parent_payment=None, #Obvious
                address_index=None,# Use a particular address index for this payment
                reuse_address=None) #Used previously paid address for this payment  
    pid = payment.id
    return redirect(f"/paydetails/payment/{pid}")


def about(request):
    return render(request, "core/about.html")

def services(request):
    return render(request, "core/services.html")

def price(request):
    return render(request, "core/price.html")

def terms(request):
    return render(request, "core/terms.html")

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        print("posted")
        if form.is_valid():
            print()
            print("form is valid")
            print()
            subject = form.cleaned_data.get('subject')
            message =f"Message from:{form.cleaned_data.get('email')}:\n{form.cleaned_data.get('snd_message')}" 
            recipient = ADMIN_MAIL
            send_mail(subject, message, EMAIL_HOST_USER, (recipient,), fail_silently=False)
            messages.Info(request, "Thank you for reaching out to us. You would be responded to as soon as possible")
            return redirect("core:home")
    return render(request, "core/contact.html", {'form':form})

