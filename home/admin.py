from django.contrib import admin
from .models import Category, UnitMeasure,Product

# Register your models here.

admin.site.register(Category)
admin.site.register(UnitMeasure)
admin.site.register(Product)