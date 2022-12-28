from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone','adress_line1', 'adress_line2','country',
        'city', 'order_note']
