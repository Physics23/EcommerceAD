from django.contrib import admin
from .models import Payement, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payement','user','product', 'quantity','product_price', 'ordered')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'fullname','phone','email','tax','status','is_ordered','created_at']
    list_filter =['status','is_ordered']
    search_fields = ['order_number','first_name','last_name','email','phone']
    list_per_page =20
    inlines =[OrderProductInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(Payement)
admin.site.register(OrderProduct)
