from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Auto-populate slug based on name

#Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'seller', 'price', 'date_posted')
    list_filter = ('category', 'date_posted', 'seller') # Allow filtering in admin
    search_fields = ('name', 'description') # Allow searching
