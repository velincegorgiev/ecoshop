from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('account/', include('account.urls', namespace='account')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('order/', include('order.urls', namespace='order')),
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),
]

handler404 = "account.views.page_not_found_view"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
