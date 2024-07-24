from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Device, Refurbishment, QualityAssurance, CustomerSupport, Product, Cart, CartItem, Order, OrderItem, EnquiryModel, UserProfile

admin.site.register(Device)
admin.site.register(Refurbishment)
admin.site.register(QualityAssurance)
admin.site.register(CustomerSupport)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(EnquiryModel)
admin.site.register(UserProfile)