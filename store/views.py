from django.shortcuts import render,get_object_or_404
from  .models import Product
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
        product_count=products.count()
    else:    
        products=Product.objects.all().filter(is_avaible=True)
        product_count=products.count()
    context={
        'products':products,
        'product_count':product_count,
    }
    return render(req,'store/store.html',context)

def product_detail(req,category_slug,product_slug):
    # how we get the accessed to the category id 
    # find the product that matches both the category slug and the product slug in db
    try:
        # __ double underscore tells django to looks through the related category field and checks its slugh field
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    except  Exception as e:
        raise e  
    
    context={
        'single_product':single_product,
    }
    return render(req,'store/product_detail.html',context)
