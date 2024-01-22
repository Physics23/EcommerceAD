from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm
from .models import Product, ProductGallery
from orders.models import OrderProduct
from store.models import ReviewRating
from django.contrib import messages
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem, Cart
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.all().filter(category = categories, is_available=True)
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available =True).order_by('id')
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context =  {
<<<<<<< HEAD
        'products': paged_products,
        'product_count':product_count
        }
=======
     'products': paged_products,
     'product_count':product_count
    }
>>>>>>> f2e9e8b17a61506fe9d47690ff42aa78b7fecbd7
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug , product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug , slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e
    # check if the user has purshached the product or not.
    try:
        orderproduct = OrderProduct.objects.filter(user=request.user.id, product_id = single_product.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct = none
    #get reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status =True)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {'single_product':single_product,
                'in_cart':in_cart,
                'orderproduct': orderproduct,
                'reviews':reviews,
                'product_gallery': product_gallery
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_date').filter(Q(description__icontains =keyword)|Q(product_name__icontains =keyword)).order_by('id')
            product_count = products.count()
        context = {'products': products , 'product_count':product_count}

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method== 'POST':

        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id )
            form = ReviewForm(request.POST, instance = reviews)
            form.save()
            messages.success(request, 'Thank you your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, your review have been submited')
                return redirect(url)
