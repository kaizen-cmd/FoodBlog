from django.db import models
from django.utils.text import slugify
import datetime
from django.contrib.auth.models import User
from recipe.models import Recipe

# Create your models here.

class Email(models.Model):
    email = models.TextField(unique=True)
    def __str__(self):
        return self.email

class Comment(models.Model):
    user = models.ManyToManyField(to=User, blank=True)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

class KeyWord(models.Model):
    keyword = models.TextField(unique=True)
    def __str__(self):
        return self.keyword

class Category(models.Model):
    category = models.TextField()
    img = models.URLField()

    def __str__(self):
        return self.category

class BlogPost(models.Model):
    title = models.TextField(unique=True)
    slug = models.SlugField(default='', blank=True)
    meta_descreption = models.TextField(max_length=155)
    feat_img = models.URLField()
    body = models.TextField()
    author = models.TextField(default='ShefHat')
    keywords = models.ManyToManyField(to=KeyWord)
    category = models.ManyToManyField(to=Category)
    date = models.DateField(blank=True)
    time_to_read = models.CharField(max_length=2)
    comments = models.ManyToManyField(to=Comment, blank=True)
    published = models.BooleanField(default=False)
    recipe = models.ManyToManyField(to=Recipe, blank=True)
    shares = models.IntegerField(blank=True, default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.date = datetime.date.today()
        #send mail code here
        super().save(*args, **kwargs)
