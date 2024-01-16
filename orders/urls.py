from django.urls import path
from . import views
from orders import views

urlpatterns = [
    path('placeorder/', views.placeorder, name ='placeorder'),
    path('payements/', views.payements, name = 'payements'),
    path('order_complete/', views.order_complete, name ='order_complete'),

]
