from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from cryptocurrency_payment.models import CryptoCurrencyPayment

CATEGORY_CHOICES = (
    ('BS', 'Brass Plan'),
    ('BP', 'Bronze Plan'),
    ('SP', 'Silver Plan'),
    ('GP', 'Gold Plan')
)
LABEL_CHOICES = (
    ('ASP', 'A Starter Pack'),
    ('MP', 'Most Popular'),
    ('INV', 'Invest More, Earn More'),
    ('AHF', 'Higher Features You Will Need'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    label = models.CharField(choices=LABEL_CHOICES, max_length=3)
    max_price = models.FloatField()
    min_price = models.FloatField()
    to_pay = models.FloatField(blank=True, null=True)
    slug = models.SlugField()
    description1 = models.CharField(max_length=30)
    description2 = models.CharField(max_length=30)
    description3 = models.CharField(max_length=30)
    description4 = models.CharField(max_length=30)
    description5 = models.CharField(max_length=30)
    description6 = models.CharField(max_length=30, null=True, blank=True)
    # description7 = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} on {self.item.title} plan'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Withdraw(models.Model):
    is_able = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.pk}"


class PlanGrowth(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE) 
    amount = models.FloatField(default=0.0)