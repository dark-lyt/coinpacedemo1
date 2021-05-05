from account.models import Profile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistratioinForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from core.models import Item
from cryptocurrency_payment.models import CryptoCurrencyPayment


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
    return render(request, 'core/index-2.html')

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


def transaction(request):
    try:
        history = CryptoCurrencyPayment.objects.filter(user=request.user).order_by('-created_at')
        return render(request, "core/crypto-transactions.html", {'history':history})
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("core:home")