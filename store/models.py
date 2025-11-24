from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products')
    Stock=models.IntegerField()
    is_avaible=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    # reversed function generate the url for the view name product details instead of hard codeing
    # have to passed two argument category and slug

    def __str__(self):
        return self.product_name
    
class VariationManager(models.Manager):
    # It finds all active variations where the category is “color”.
    def colors(self):
        return super(VariationManager, self).filter(
            variation_category='color',
            is_active=True
        )

    def sizes(self):
        return super(VariationManager, self).filter(
            variation_category='size',
            is_active=True
        )
   
    # make dropdown value
variation_category_choice=(
    ('color','color'),
    ('size','size')
)
class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    # tell that we have made variation model
    # tell django to use your custome manager so u can call color and sizes
    objects=VariationManager()

    def __str__(self):
        return self.variation_value



