from django.contrib import admin
from .models import Category, Book, Order

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Order)
