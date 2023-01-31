from django.contrib import admin
from .models import Payment, Order, OrderProduct
from django.utils.html import format_html


# class OrderProdcutInline(admin.TabularInline):
#     # def thumbnail(self, object): 'thumbnail',
#     #     return format_html('<img src="{}" width="75" height="110">'.format(object.product.image.url))
#     # thumbnail.short_description = 'Product Picture'
#     model = OrderProduct
#     readonly_fields = ['product','variations','product_price', 'quantity','user','payment',    'ordered',  ]
#     extra = 0

class OrderProdcutInline(admin.TabularInline):
    def thumbnail(self, object):
        return format_html('<img style="border-radius:10px; width:100px; height:100px" src="{}">'.format(object.product.image.url))
    thumbnail.short_description = 'Product Picture'
    model = OrderProduct
    readonly_fields = ['thumbnail','product','variations','product_price', 'quantity','user','payment',    'ordered',  ]
    extra = 0
    
admin.site.register(Payment)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'phone', 'order_total', 'status', 'is_ordered' ]
    list_filter = ['is_ordered', 'status']
    list_per_page = 20
    inlines = [OrderProdcutInline]
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']


admin.site.register(OrderProduct)