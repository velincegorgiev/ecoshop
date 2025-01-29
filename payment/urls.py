from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.basket_view, name='basket_view'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('error/', views.error_view, name='error'),
    path('webhook/', views.stripe_webhook),
]
