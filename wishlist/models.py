from django.conf import settings
from django.db import models

from store.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users_wish', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_wish', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)
