from django.shortcuts import render, redirect
from carts.models import CartItem
from django import forms
from .forms import OrderForm
from .models import Order, Payement
from datetime import datetime
import datetime
from datetime import date
import json

def payement(request):
    body = json.load(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    print(order)
    #store information payement inside payement models
    payement = Payement(
    user= request.user,
    payement_id = body['transID'],
    payement_method = body['payement_method'],
    amount_paid = order.order_total,
    status = body['status'],
    )
    payement.save()
    order.payement = payement
    order.is_ordered = True
    order.save()
    #store transactions details inside the payements models

    #move order cartitem to the order productdertable
    # reduce the quantity of sold products
    # clear the carts
    # send an order received email to the customer
    # send order number and transaction id back to senddata method via jsonResponse

    return render(request, 'orders/payements.html')

def placeorder(request, quantity = 0, total = 0):
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
                total =+  (cart_item.product.price*cart_item.quantity)
                quantity+= (cart_item.quantity)
                tax = (2*total)/100
                grandtotal = total+tax
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
           yr = int(datetime.date.today().strftime('%Y'))
           dt = int(datetime.date.today().strftime('%d'))
           mt = int(datetime.date.today().strftime('%m'))
           d = datetime.date(yr,mt,dt)
           current_date = d.strftime("%Y%m%d")
           order_number = current_date + str(data.id)
           data.order_number = order_number
           data.save()

           order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)

           context = {
           'order':order,
           'tax':tax,
           'total':total,
           'cart_items':cart_items,
           'grandtotal':grandtotal,
           }
           return render(request, 'orders/payements.html', context)
       else:
           return redirect('payement')


    #return render(request, 'orders/placeorder.html')
