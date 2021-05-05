from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from cryptocurrency_payment.models import CryptoCurrencyPayment

CATEGORY_CHOICES = (
    ('BP', 'Baby Plan'),
    ('AP', 'Advanced Plan'),
    ('LP', 'Luxury Plan'),
    ('LgP', 'Legend Plan')
)
LABEL_CHOICES = (
    ('DAM', 'Dedicated Account Manager'),
    ('SAM', 'Senior Account Manager'),
    ('PRM', 'Personal Relational Manager'),
)
# ADDRESS_CHOICES = (
#     ('B', 'billing'),
#     ('S', 'shipping')
# )


# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     stripe_customer_id = models.CharField(max_length=20, blank=True, null=True)
#     one_click_purchasing = models.BooleanField()

#     def __str__(self):
#         return self.user.username


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
    description6 = models.CharField(max_length=30)
    description7 = models.CharField(max_length=30)

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
    ref_code = models.CharField(max_length=20, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Withdraw(models.Model):
    order = models.ForeignKey(CryptoCurrencyPayment, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)
    amount = models.IntegerField()
    def __str__(self):
        return f"{self.pk}"

