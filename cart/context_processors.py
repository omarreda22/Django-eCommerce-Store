# from .models import Category
# 
# def category_list(request):
#     return {
#         'categories' : Category.objects.all(),
#     }
# 
# from .models import Category
# 
# def menu_links(request):
#     links = Category.objects.all()
#     return dict(links=links)
# 
# 
# from .models import Cart, CartItem
# from .views import _cart_id
# 
# def counter(request):
#     cart_count = 0
#     if 'admin' in request.path:
#         return {}
#     else :
#         try:
#             cart = Cart.objects.filter(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.all().filter(cart=cart[:1])
#             for cart_item in cart_items:
#                 cart_count += cart_item.quantity
#         except Cart.DoesNotExist:
#             cart_count = 0
#     return dict(cart_count=cart_count)


from .models import Cart, CartItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist


def counter(request):
    cart_count = 0
    
    total_price=0
    quantity=0
    cart_items=None
    grand_total = 0
    tax = 0
    cart_itemsss = None

    if 'admin' in request.path:
        return {}
    else :
        try:
            # cart = Cart.objects.filter(cart_id=_cart_id(request))
            # cart_items = CartItem.objects.all().filter(cart=cart[:1])
            # for cart_item in cart_items:
            #     cart_count += cart_item.quantity

            
            try:
                if request.user.is_authenticated:
                    cart_itemsss = CartItem.objects.filter(user=request.user, is_active=True)
                else:
                    carttt = Cart.objects.get(cart_id=_cart_id(request))
                    cart_itemsss = CartItem.objects.filter(cart=carttt, is_active=True)

                for cart_itemm in cart_itemsss:
                    total_price += (cart_itemm.product.price * cart_itemm.quantity)
                    quantity += cart_itemm.quantity

                
            except ObjectDoesNotExist:
                pass
            
            tax = round(((2 * total_price)/100), 2)
            grand_total = total_price + tax
            handing = 15.00
            total = float(grand_total) + handing
            
        except Cart.DoesNotExist:
            cart_count = 0

            

    return {
        'cart_count' : cart_count,
        'cart_itemsss' : cart_itemsss,
        'totalll': total_price,
        'quantityyy' : quantity,
    }