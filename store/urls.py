from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.all_products, name='all_product'),
    path('store/about', views.about, name='about'),
    path('item/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
    path('shop/', views.shop_product, name='shop')
]
