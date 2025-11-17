from django.contrib import admin
from .models import Product
# Register your models here.
# auto pre populate fields
class ProductAdmin(admin.ModelAdmin):
      list_display=('product_name','price','Stock','category','modified_date')
      prepopulated_fields={'slug':('product_name',)}


admin.site.register(Product,ProductAdmin)