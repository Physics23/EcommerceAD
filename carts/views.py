from django.shortcuts import render, redirect, get_object_or_404
from . import views
from store.models import Product
from .models import CartItem, Cart
from store.models import Variation
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



#################################################3
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id = product_id)
    #if user is is_authenticated
    if current_user.is_authenticated:
        product_variation = []  # inside this list we will have color and size, ex: red, small
        if request.method == 'POST':
            #color = request.POST['color']
            #size =request.POST['size']
            #for loop for the genearal case
            for item in request.POST:
                key = item
                value = request.POST[key]
                # check if key and value maches the variation models values
                #print(color,size)
                try:
                    variation = Variation.objects.get(product= product, variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                    #first we check if product_variation is empty or not
                except:
                    pass


        is_cart_items_exists = CartItem.objects.filter(product=product, user =current_user).exists()

        if is_cart_items_exists:
            cart_item = CartItem.objects.filter(product = product , user = current_user) # conbine cart and product, become cartitem.
            #first we check if product_variation is empty or not by using the len()
            ex_var_list =[]
            id =[]
            for item in cart_item:
                existing_var = item.variations.all()
                ex_var_list.append(list(existing_var))
                id.append(item.id)


            if product_variation in ex_var_list:
                #increase the quantity
                index = ex_var_list.index(product_variation)
                item_id =id[index]
                item = CartItem.objects.get(product =product, id = item_id)
                item.quantity +=1
                item.save()
            else:
                #create the a new cartitem.
                if len(product_variation) > 0:

                   item = CartItem.objects.create(product=product, quantity =1, user=current_user)
                   item.variations.clear()
                   item.variations.add(*product_variation)
                   item.save()

        else:
            cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            user = current_user,
            )

            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                item.save()
        return redirect('cart')
        ######################
        #if user is not autenticated
    else:
        product_variation = []  # inside this list we will have color and size, ex: red, small
        if request.method == 'POST':
            #color = request.POST['color']
            #size =request.POST['size']
            #for loop for the genearal case
            for item in request.POST:
                key = item
                value = request.POST[key]
                # check if key and value maches the variation models values
                #print(color,size)
                try:
                    variation = Variation.objects.get(product= product, variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                    #first we check if product_variation is empty or not
                except:
                    pass



        try:
            cart = Cart.objects.get(cart_id =_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
            cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_items_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_items_exists:
            cart_item = CartItem.objects.filter(product = product , cart = cart) # conbine cart and product, become cartitem.
            #first we check if product_variation is empty or not by using the len()
            ex_var_list =[]
            id =[]
            for item in cart_item:
                existing_var = item.variations.all()
                ex_var_list.append(list(existing_var))
                id.append(item.id)


            if product_variation in ex_var_list:
                #increase the quantity
                index = ex_var_list.index(product_variation)
                item_id =id[index]
                item = CartItem.objects.get(product =product, id = item_id)
                item.quantity +=1
                item.save()
            else:
                #create the a new cartitem.
                if len(product_variation) > 0:

                   item = CartItem.objects.create(product =product, quantity =1, cart =cart)
                   item.variations.clear()
                   item.variations.add(*product_variation)
                   item.save()

        else:
            cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
            )

            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                item.save()
        return redirect('cart')


##############################################################################
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id =product_id)

    try:
        # remove cart for logged in user
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user = request.user, id = cart_item_id)
        else:
            # for non looged  in user
           cart = Cart.objects.get(cart_id = _cart_id(request))
           cart_item = CartItem.objects.get(product=product, cart = cart, id = cart_item_id)
##############################################################################
        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

###############################################################################
def remove_cartitem(request, product_id, cart_item_id):
    #cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id =product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product= product, user=request.user, id = cart_item_id )
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product= product, cart = cart, id = cart_item_id )
        ######################################################
    cart_item.delete()
    return redirect('cart')





##################################################################################
def cart(request, total=0, quantity =0, tax =0, grandtotal=0, cart_items = None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active =True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart= cart, is_active =True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += (cart_item.quantity)
        tax = (2*total)/100
        grandtotal = total+tax
    except ObjectDoesNotExist:
        pass

    context = {
     'total':total,
     'quantity':quantity,
     'cart_items':cart_items,
     'tax':tax,
     'grandtotal':grandtotal,
    }
    return render(request, 'store/cart.html', context)

#############################################################################################33\
@login_required(login_url ='login')
def checkout(request, total=0, quantity =0, tax = 0, grandtotal=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active =True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += (cart_item.quantity)
        tax = (2*total)/100
        grandtotal = total+tax
    except ObjectDoesNotExist:
        pass

    context = {
     'total':total,
     'quantity':quantity,
     'cart_items':cart_items,
     'tax':tax,
     'grandtotal':grandtotal,
     }
    return render(request, 'store/checkout.html', context)
