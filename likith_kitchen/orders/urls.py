from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('success/', views.success),
    path('orders/', views.order_history),
]
