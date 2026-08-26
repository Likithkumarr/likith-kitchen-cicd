from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart),
    path('cart/', views.cart_view),
    path('apply-coupon/', views.apply_coupon),
    path('toggle-theme/', views.toggle_theme),
]
