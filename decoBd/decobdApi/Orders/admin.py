# from django.contrib import admin
# from Orders.models import Order,OrderItem
# from django.utils.html import format_html
# Register your models here.
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id','user','get_order_items','shipping_address','total_price','payment_status','paid_amount')
#     inlines = [OrderItemInline]

#     def get_shipping_address(self, obj):
#         if obj.shipping_address:
#             return obj.shipping_address.address
#         else:
#             return ''
#     get_shipping_address.short_description = 'Shipping Address'


#     def get_order_items(self, obj):
#         return ", ".join([str(item.product) for item in obj.order_items.all()])
#     get_order_items.short_description = 'Order Items'


# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'get_order_items', 'get_mobile_number', 'shipping_address', 'total_price', 'payment_status', 'paid_amount')
#     inlines = [OrderItemInline]

#     def get_shipping_address(self, obj):
#         if obj.shipping_address:
#             return obj.shipping_address.address
#         else:
#             return ''
#     get_shipping_address.short_description = 'Shipping Address'

#     def get_mobile_number(self, obj):
#         if obj.shipping_address:
#             return obj.shipping_address.mobile_number  # Assuming the shipping address model has a mobile_number field
#         return ''
#     get_mobile_number.short_description = 'Mobile Number'

#     def get_order_items(self, obj):
#         items = obj.order_items.all()
#         return format_html(
#             "<br/>".join([
#                 f'<div>{item.product.name}<br/><img src="{item.product.images.url}" style="max-height: 50px; max-width: 50px;" /></div>'
#                 for item in items
#             ])
#         )
#     get_order_items.short_description = 'Order Items'

# admin.site.register(Order,OrderAdmin)  
# admin.site.register(OrderItem)      


from django.utils.html import format_html
from django.contrib import admin
from Orders.models import Order, OrderItem
from Products.models import ProductImage  # Assuming ProductImage is in Products app

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_order_items', 'get_mobile_number', 'get_shipping_address', 'total_price', 'payment_status', 'paid_amount','get_panding_amount')
    inlines = [OrderItemInline]

    @admin.display(description='Shipping Address')
    def get_shipping_address(self, obj):
        if obj.shipping_address:
            return f"{obj.shipping_address.address}, {obj.shipping_address.city}, {obj.shipping_address.country}"
        return ''

    @admin.display(description='Phone Number')
    def get_mobile_number(self, obj):
        if obj.shipping_address:
            return obj.shipping_address.phone
        return ''
    
    @admin.display(description='Pending Amount')
    def get_panding_amount(self,obj):
        return obj.after_partial_cod_remain_total_price

    @admin.display(description='Order Items')
    def get_order_items(self, obj):
        items = obj.order_items.all()
        result = []
        
        for item in items:
            product_images = item.product.product_imgs.all()
            if product_images.exists():
                image_url = product_images.first().images.url  # Use the first image
            else:
                image_url = ''  # Fallback if no image is available

            # Arrange the image and name side by side
            result.append(format_html(
                '<div style="display: flex; align-items: center; margin-bottom: 10px;">'
                '<img src="{}" style="max-height: 40px; max-width: 40px; border-radius: 50%; margin-right: 10px;" />'
                '<span>{}</span>'
                '</div>',
                image_url, item.product.name
            ))
        
        return format_html(''.join(result))

admin.site.register(Order, OrderAdmin)

