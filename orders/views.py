from django.shortcuts import render, redirect
from carts.models import CartItem
from django import forms
from .forms import OrderForm
from .models import Order
import datetime

def payement(request):
    return render(request, 'orders/payements.html')

def placeorder(request):
    current_user = request.user
    # if cartcount is equal or less to zero, then redirect to shop
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store')
    ############################################
    if request.method == 'POST':
       form = OrderForm(request.POST)
       if form.is_valid():
           data = Order()
           grand_total = 0
           tax = 0
           cart_items = CartItem.objects.filter(user = current_user)
           for cart_item in cart_items:
                total =+  (CartItem.product.price*cart_item*price)
                quantity+= cart_item.quantity
                tax = (2*total)/100
                grand_total = total+tax
        #store all the billing information in the ordertable
           data.user = current_user
           data.first_name = form.cleaned_data['first_name']
           data.last_name = form.cleaned_data['last_name']
           data.email = form.cleaned_data['email']
           data.phone = form.cleaned_data['phone']
           data.adress_line1 = form.cleaned_data['adress_line1']
           data.adress_line2 = form.cleaned_data['adress_line2']
           data.country = form.cleaned_data['country']
           data.state = form.cleaned_data['state']
           data.city = form.cleaned_data['city']
           data.order_note = form.cleaned_data['order_note']
           data.order_total = grand_total
           data.tax = tax
           data.ip = request.META.get('REMOTE_ADDR')
           data.save()
        # Generate order_number
           yr = int(datatime.date.today().strftime('% Y'))
           dt = int(datatime.date.today().strftime('% d'))
           my = int(datatime.date.today().strftime('% m'))
           d = datetime.date(yr,dt,mt)
           current_date = d.strftime("%Y%m%d")
           order_number = current_date + str(data.id)
           data.order_number = order_number
           data.save()
           return redirect('checkout')
       else:
           return redirect('checkout')


    return render(request, 'orders/placeorder.html')
