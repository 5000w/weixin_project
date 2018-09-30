from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('get_coupon', views.get_coupon, name='get_coupon'),
    path('set_coupon_sta', views.set_coupon_sta, name='set_coupon_sta'),

    path('share_for_coupon',views.share_for_coupon,name='share_for_coupon'),

    path('get_all_goods', views.get_all_goods, name='get_all_goods'),
    path('payOrder', views.payOrder, name='payOrder'),
    path('payback', views.payback, name='payback'),

]
