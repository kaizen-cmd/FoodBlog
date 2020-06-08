from django.contrib import admin
from . import models

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')

admin.site.register(models.BlogPost, BlogAdmin)
admin.site.register([models.KeyWord, models.Comment, models.Email, models.Category])