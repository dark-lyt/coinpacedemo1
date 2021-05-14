from account.models import Profile
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistratioinForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from core.models import Item, Withdraw
from core.forms import WithdrawForm
from cryptocurrency_payment.models import CryptoCurrencyPayment
from coinpace.settings import EMAIL_HOST_USER
from django.core.mail import message, send_mail

ADMIN_MAIL = 'amoakbeall@fuwari.be'

def register(request):
    if request.method == 'POST':
        user_form = UserRegistratioinForm(request.POST, request.FILES)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the user object
            
            new_user.save()
            
            country = user_form.cleaned_data['country']
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            print(country)
            photo = user_form.cleaned_data['photo']
            phone_number = user_form.cleaned_data['phone_number']
            Profile.objects.create(user=new_user, country=country, photo=photo, phone_number=phone_number)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("core:home")
        else:
            return render(request, 'account/register.html', {'form': user_form, 'error':user_form.errors})
            
    else:
        user_form = UserRegistratioinForm()
    return render(request, 'account/register.html',{'form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    total = 0
    total_usd = 0
    history = CryptoCurrencyPayment.objects.filter(user=request.user).order_by('-created_at')
    for history in history:
        if history.status == 'paid':
            total += history.crypto_amount
            total_usd += history.fiat_amount
    form = WithdrawForm(request.POST or None)
    if form.is_valid():
        address = form.cleaned_data.get('address')
        amount = form.cleaned_data.get('amount')
        amount = int(amount)
        # if amount > 0 and amount<= total_usd:
        if amount > 0:
            subject = form.cleaned_data.get('subject')
            message =f"Message from:{request.user}:\n{request.user} wishes to withdraw {amount} worth of btc from thier investment to\
                the address: {address}" 
            recipient = ADMIN_MAIL
            # send_mail(subject, message, EMAIL_HOST_USER, [recipient   ], fail_silently=False)
            send_mail("Withdrawal Request: COINPACE", f"Your request for {amount} worth of BTC from\
                your investment has been recieved and will be sent to the address:\
                     {address} as you have provided with in the next 24hrs.\
                    Thank you for investing with us.", EMAIL_HOST_USER, request.user.email, fail_silently=False)
            messages.info(request, "Your request has been recieved")
            withdraw = Withdraw.objects.create(user=request.user, amount=amount)
            withdraw.save()
            return redirect("core:home")
        else:
            messages.info(request, "You are not able to withdraw at the moment")
    return render(request, 'core/index-2.html', {'total':total, "total_usd":total_usd, "form":form })

@login_required
def invest(request):
    item_list = Item.objects.all()
    return render(request, "core/transaction.html", {'item_list':item_list})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error while updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def transaction(request):
    try:
        history = CryptoCurrencyPayment.objects.filter(user=request.user).order_by('-created_at')
        return render(request, "core/crypto-transactions.html", {'history':history})
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("core:home")