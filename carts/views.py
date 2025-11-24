from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cart,Cart_item
from django.http import HttpResponse
from django.http import HttpResponse

# Create your views here.
# to get session id
# __meaning private fucntion does not used outside its module or class
def _cart_id(req):
    cart=req.session.session_key
    if not cart:
        cart=req.session.create()
    return cart

def add_cart(req, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    if req.method == "POST":
        # loop through submitted form data for variations
        for key in req.POST:
            value = req.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get  the cart
    # Get the cart (fixed)
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(req))


    # Check if cart item exists for this product
    cart_items = Cart_item.objects.filter(product=product, cart=cart)

    if cart_items.exists():
        ex_var_list = []
        id_list = []

        # Build list of existing variations
        for item in cart_items:
            existing_variation = list(item.variation.all())
            ex_var_list.append(existing_variation)
            id_list.append(item.id)

        # If the exact variation exists, increase quantity
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id_list[index]
            cart_item = Cart_item.objects.get(product=product, id=item_id)
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Create new cart item with this variation
            cart_item = Cart_item.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if product_variation:
                for var in product_variation:
                    cart_item.variation.add(var)
            cart_item.save()
    else:
        # No cart item exists, create a new one
        cart_item = Cart_item.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        if product_variation:
            for var in product_variation:
                cart_item.variation.add(var)
        cart_item.save()

    return redirect('cart')

       
#  decrease
def remove_cart(req,product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(req))
    product=get_object_or_404(Product,id=product_id)
    try:
        cart_item=Cart_item.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete() 
    except:
        pass           
    return redirect('cart')    

 
# reomve item  from the card 
def remove_cart_item(req,product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(req))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cart_item.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(req):
    total=0
    quantity=0
    cart_items=[]
    try:
        cart=Cart.objects.get(cart_id=_cart_id(req))
        # Get all active items in the cart.
        cart_items=Cart_item.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price* cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100  
        grand_total=total+tax
    except  Cart_item.DoesNotExist:
        pass 
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }   
   
    return render(req,'store/cart.html',context)
