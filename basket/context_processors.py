from .basket import Basket


def basket(request):
    basket = Basket(request)
    total_price = basket.get_total_price()
    return {'basket': basket, 'basket_total_price': total_price}
