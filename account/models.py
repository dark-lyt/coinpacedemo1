from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    country = CountryField(null=True)
    photo = models.ImageField(upload_to='images/', blank=True)
    phone_number = PhoneNumberField(null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)



# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()