from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from  .models import Product
from  carts.models import Cart_item
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q


from category.models import Category
# Create your views here.
# filtering the product
def store(req,category_slug=None):
    categories=None
    products=None
    # check if category slug is given in the url if yes filter products by that category
    # if not we show all  products
    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        
        products=Product.objects.filter(category=categories,is_avaible=True)
        paginator=Paginator(products,1) 
        page=req.GET.get('page') 
        paged_products=paginator.get_page(page)
        product_count=products.count()
    else: 
        # get all product   
        products=Product.objects.all().filter(is_avaible=True).order_by('id')
        # paginator:no. of product u want to show
        # take 6 product
        paginator=Paginator(products,3) 
        page=req.GET.get('page') 
        paged_products=paginator.get_page(page)
        product_count=products.count()
        
    context={
        'products':paged_products,
        'product_count':product_count,
    }
    return render(req,'store/store.html',context)

def product_detail(req,category_slug,product_slug):
    # how we get the accessed to the category id 
    # find the product that matches both the category slug and the product slug in db
    try:
        # __ double underscore tells django to looks through the related category field and checks its slugh field
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = Cart_item.objects.filter(cart__cart_id=_cart_id(req),product=single_product).exists()
        # Find all cart items where the cart’s cart_id matches the current session’s cart_id.
  
    except  Exception as e:
        raise e  
    
    context={
        'single_product':single_product,
        'in_cart':in_cart
    }
    return render(req,'store/product_detail.html',context)

def search(req):
    # first checking if it has keyword then if it has then store in teh keyword i mean value
    if 'keyword' in req.GET:
        keyword=req.GET['keyword']
        if keyword:
            # It finds all products whose description contains the keyword=__icontains
           products = Product.objects.order_by('-created_date').filter(  Q(description__icontains=keyword) | Q(product_name__icontains=keyword))  
           product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(req,'store/store.html',context)

