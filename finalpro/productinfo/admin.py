from django.contrib import admin

from productinfo.models import Category, Shipping_Method, Payment_Method, Customer, Product, Shopping_Cart, Cart_Item, \
	Order, Order_Product

admin.site.register(Category)
admin.site.register(Shipping_Method)
admin.site.register(Payment_Method)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Shopping_Cart)
admin.site.register(Cart_Item)
admin.site.register(Order)
admin.site.register(Order_Product)