from rest_framework import serializers
from .models import Product, ProductImage, FeaturedProduct
from CategoryAndSubcategory.serializers import CategorySerializer, SubCategorySerializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'images')

class ProductSerializer(serializers.ModelSerializer):
    description = serializers.ReadOnlyField()
    product_imgs = ProductImageSerializer(many=True)
    Category = CategorySerializer(read_only=True)
    Sub_category = SubCategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'discount_price', 'description', 'Category', 'Sub_category', 'tags', 'stock','product_imgs')

class FeaturedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = FeaturedProduct
        fields = ('id', 'product')