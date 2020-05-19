from django.contrib import admin
from .models import Recipe, Ingredient, Tag, BlogPost, Category

# Register your models here.

admin.site.register(Recipe)
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Category)