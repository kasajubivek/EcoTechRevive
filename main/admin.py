from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Device, Refurbishment, QualityAssurance, CustomerSupport, Product

admin.site.register(Device)
admin.site.register(Refurbishment)
admin.site.register(QualityAssurance)
admin.site.register(CustomerSupport)
admin.site.register(Product)