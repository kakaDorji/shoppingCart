from django.contrib import admin
from .models import Category

# Register your models here.
# to make autopopulate fields
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Category_name',)}
    list_display=('Category_name','slug')


# register here for autopopulate
admin.site.register(Category,CategoryAdmin)