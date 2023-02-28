from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from carts.models import CartItem
from django import forms
from .forms import OrderForm
from .models import Order, Payement, OrderProduct
from datetime import datetime
import datetime
from datetime import date
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import json

def payements(request):
    body = json.loads(request.body)
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
    #move order cartitem to the order productdertable
    cart_item = CartItem.objects.filter(user = request.user)
    for item in cart_item:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payement = payement
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordererd = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
    # reduce the quantity of sold products
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear the carts
    CartItem.objects.filter(user = request.user).delete()
    # send an order received email to the customer
    mail_subject ='thank you for your order'
    message = render_to_string('orders/order_received_email.html' ,{
     'user': request.user,
     'order': order,

     })

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to =[to_email])
    send_email.send()
    # send order number and transaction id back to senddata method via jsonResponse
    data = {
      'order_number': order.order_number,
      'transID': payement.payement_id,
    }

    return JsonResponse(data)



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
           data.order_total = grandtotal
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
           return redirect('checkout')


    #return render(request, 'orders/placeorder.html')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payement_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        orderproducts = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in orderproducts:
            subtotal+= i.product_price*i.quantity
        payement = Payement.objects.get(payement_id=transID)
        context = {
        'order':order,
        'orderproducts':orderproducts,
        'order_number':order.order_number,
        'transID':payement.payement_id,
        'payement':payement,
        'subtotal':subtotal,
        }
        return render(request, 'orders/order_complete.html', context)

    except(Payement.DoesNotExist, Order.DoesNotExist):
       return redirect('home')
