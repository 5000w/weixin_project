from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('get_coupon', views.get_coupon, name='get_coupon'),
    path('set_coupon_sta', views.set_coupon_sta, name='set_coupon_sta'),

    path('share_for_coupon',views.share_for_coupon,name='share_for_coupon'),
    path('get_class',views.get_class,name='get_class'),
    path('get_all_goods', views.get_all_goods, name='get_all_goods'),
    path('payOrder', views.payOrder, name='payOrder'),
    path('payback', views.payback, name='payback'),
    path('add_order', views.add_order, name='add_order'),
    path('get_order_detail', views.get_order_detail, name='get_order_detail'),
    path('download_txt', views.download_txt, name='download_txt'),
    path('initialize_conpon', views.initialize_conpon, name='initialize_conpon'),
    path('clear_txt',views.clear_txt,name="clear_txt"),
    path('check_by_sid',views.check_by_sid,name="check_by_sid"),
]
