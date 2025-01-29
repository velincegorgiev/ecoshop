from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .models import Wishlist


@login_required
def view_list(request):
    user_id = request.user.id
    wishlist = Wishlist.objects.filter(user=user_id)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})


def add_wish(request):
    if request.method == 'POST':
        user_id = request.user.id
        product_id = request.POST.get('product_id')
        product_wish = get_object_or_404(Product, id=product_id)
        if Wishlist.objects.filter(product=product_wish, user=user_id).exists():
            response = JsonResponse({'not done': 'object already in wishlist'})
            return response

        else:
            Wishlist.objects.create(user_id=user_id, product=product_wish)
            response = JsonResponse({'success': 'Return something'})
            return response


def delete_wish(request):
    if request.method == 'POST':
        wishlist_id = request.POST.get('wish_id')
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        wishlist.delete()
        response = JsonResponse({'success': 'Return something'})
        return response
