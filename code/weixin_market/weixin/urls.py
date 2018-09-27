from django.urls import path
from . import views

urlpatterns = [
    path('get_coupon', views.user_login, name='get_coupon'),
    path('login', views.get_coupon, name='login'),
    path('set_coupon_sta', views.set_coupon_sta, name='set_coupon_sta'),
]
