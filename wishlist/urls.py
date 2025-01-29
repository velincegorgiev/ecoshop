from django.urls import path

from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.view_list, name='list'),
    path('add/', views.add_wish, name='add'),
    path('delete/', views.delete_wish, name='delete_wish'),
]
