from django.contrib import admin

from .models import Item, Order, OrderItem
#  Address, Payment, Coupon, Refund, UserProfile


# def make_request_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)

# make_request_accepted.short_description = "Update orders to refund granted"


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user',
#                     'ordered',]

#     list_filter = ['ordered',
#                    'being_delivered',
#                    'recieved',
#                    'refund_requested',
#                    'refund_granted'
#                    ]

#     list_display_links = [
#         'billing_address',
#         'shipping_address',
#         'payment',
#         'coupon',
#     ]

#     search_fields = [
#         'user__username',
#         'ref_code',
#     ]

#     actions = [
#         make_request_accepted
#     ]


# class AddressAdmin(admin.ModelAdmin):
#     list_display = [
#         'user',
#         'street_address',
#         'appartment_address',
#         'country',
#         'zip',
#         'address_type',
#         'default'
#     ]

#     list_filter = [
#         'default',
#         'address_type',
#         'country'
#     ]

#     search_fields = [
#         'user',
#         'street_address',
#         'appartment_address',
#         'zip'
#     ]



admin.site.register(Item)
# admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Address, A)
# admin.site.register(Payment)
# admin.site.register(Coupon)
