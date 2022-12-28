from django.db import models
from accounts.models import Account
from store.models import Product, Variation


class Payement(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    payement_id = models.CharField(max_length =100)
    amount_paid = models.CharField(max_length=100)
    payement_method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.payement_id



class Order(models.Model):
    STATUS = (
     ('New', 'New'),
     ('Accepted', 'Accepted'),
     ('Completed', 'Completed'),
     ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(Account, on_delete = models.SET_NULL, null =True)
    payement = models.ForeignKey(Payement, on_delete= models.SET_NULL, blank=True, null =True)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    adress_line1 = models.CharField(max_length=100)
    adress_line2 = models.CharField(max_length=15)
    country = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    city = models.CharField(max_length=15, null = True)
    order_note = models.CharField(max_length=15, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField( max_length=100, choices = STATUS, default = 'NEW')
    ip = models.CharField( blank = True , max_length=15)
    is_ordered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    payement = models.ForeignKey(Payement, on_delete = models.SET_NULL, blank =True, null = True)
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete = models.CASCADE)
    color = models.CharField(max_length=15)
    size = models.CharField(max_length=15)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.product.product_name
