from django.core import serializers
from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from .forms import CommentForm
from .models import Category, Product


def about(request):
    return render(request, 'store/about.html')


def all_products(request):
    # Toggle product
    if request.method == "POST":
        product_id = int(request.POST.get('productid'))
        product = get_object_or_404(Product, id=product_id)
        serialized_obj = serializers.serialize('python', [product, ])
        return JsonResponse(serialized_obj, safe=False)
    else:
        all_product = Product.products.all()
        paginator = Paginator(all_product, 6)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

    return render(request, 'store/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            new_comment = comment_form.save(commit=False)
            new_comment.post = product
            new_comment.author = request.user
            comment_form.save()
            return HttpResponseRedirect(request.path_info)

    else:
        comment_form = CommentForm()

    return render(request, 'store/products/detail.html', {'product': product, 'form': comment_form})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})

def shop_product(request):
    all_product = Product.products.all()
    paginator = Paginator(all_product, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'store/shop.html', {'products': products})
