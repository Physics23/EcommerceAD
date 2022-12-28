from django.contrib import admin
from .models import Payement, Order, OrderProduct

admin.site.register(Order)
admin.site.register(Payement)
admin.site.register(OrderProduct)
