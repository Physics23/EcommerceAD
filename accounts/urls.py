from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.register, name ='register'),
    path('login/', views.login, name ='login'),
    path('logout/', views.logout, name ='logout'),
    path('dashboard/', views.dashboard, name ='dashboard'),
    path('activate/<uidb64>/<token>/',views.activate, name ='activate'),
    path('forgotpassword/', views.forgotpassword, name ='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name ='resetpassword_validate'),
    path('resetpassword/', views.resetpassword, name ='resetpassword'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('orderdetail/<int:order_id>/', views.orderdetail, name = 'orderdetail'),
    #path('contact/', views.contact, name ='contact'),

    ]
