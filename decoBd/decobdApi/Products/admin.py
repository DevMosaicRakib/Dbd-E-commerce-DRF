from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('id','name', 'discount_price', 'Category', 'Sub_category', 'stock')
    list_filter = ('Category', 'Sub_category')
    search_fields = ('name','tags')

class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name','product_category','product_discount_price')
    # search_fields = ('product__name',)

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product Name'

    def product_category(self, obj):
        return obj.product.Category.catname
    product_category.short_description = 'Product Category'

    def product_discount_price(self, obj):
        return obj.product.discount_price
    product_discount_price.short_description = 'Discount Price'       

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(FeaturedProduct, FeaturedProductAdmin)