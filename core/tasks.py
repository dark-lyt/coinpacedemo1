from __future__ import absolute_import, unicode_literals
from datetime import datetime, timezone
from celery import  shared_task
import cryptocurrency_payment
from cryptocurrency_payment.models import CryptoCurrencyPayment
from .models import OrderItem, Order, Withdraw, PlanGrowth


@shared_task()
def confirm_payment():
    print("Im working")
    cryptocurrency_payment.tasks.update_payment_status
    payments = CryptoCurrencyPayment.objects.filter(status='paid')
    for payment in payments:
        user = payment.user
        order_item = OrderItem.objects.filter(user=user, ordered=False)
        order_item.ordered = True
        order_item.save()
        ## Saving the order
        ordered_date = timezone.now
        order = Order.objects.create(
            user = user,
            ordered_date = ordered_date,
            ordered = True
        )
        order.items.add(order_item)
        order.save()


@shared_task()
def grow_plan():
    orders = Order.objects.all()
    for order in orders:
        user = order.user
        growth, created = PlanGrowth.objects.get_or_create(
            user=user,
        )
        total = growth.amount
        item_order = OrderItem.objects.filter(user=user)
        price = item_order.item.to_pay
        plan = item_order.item.slug
        # plan increament
        if plan == "brass-plan":
            interest = price * 0.25
            total += interest
            growth.amount = total
            growth.save()

        if plan == "bronze-plan":
            interest = price * 0.5
            total += interest
            growth.amount = total
            growth.save()

        if plan == "silver-plan":
            interest = price * 2
            total += interest
            growth.amount = total
            growth.save()

        if plan == "gold-plan":
            interest = price * 2
            total += interest
            growth.amount = total
            growth.save()

        qualified, created = Withdraw.get_or_create(user=user)
        delta =  datetime.today() - order.ordered_date 
        if delta.days == 3 or delta.days > 3:
            qualified.is_able = True

