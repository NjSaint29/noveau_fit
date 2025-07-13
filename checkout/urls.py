from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('wh/', views.mock_payment_webhook, name='mock_payment_webhook'),
]
