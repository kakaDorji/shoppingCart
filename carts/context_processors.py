from .models import Cart,Cart_item
from .views import _cart_id

def counter(req):
    cart_count=0
    if 'admin' in req.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(req))
            Cart_items=Cart_item.objects.all().filter(cart=cart[:1])
            for item in Cart_items:
                cart_count += item.quantity
        except Cart.DoesNotExist: 
            cart_count=0 
    return dict(cart_count=cart_count)             


