from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        serialized_queryset = serializers.serialize('python', [product, ])

        basket.add(product=product, qty=product_qty)
        return JsonResponse(serialized_queryset, safe=False)


def basket_update(request):
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_subtotal_price()
        producttotal = basket.get_price(product=product_id)
        response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal, 'ptotal': producttotal})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_subtotal_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
