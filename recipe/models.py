from django.db import models

# Create your models here.

class Tag(models.Model):
    tag = models.TextField(unique=True)

    def __str__(self):
        return self.tag

class Category(models.Model):
    category = models.TextField(unique=True)

    def __str__(self):
        return self.category

class Ingredient(models.Model):
    ingredient = models.TextField(unique=True)

    def __str__(self):
        return self.ingredient

class Step(models.Model):
    step = models.TextField(unique=True)

    def __str__(self):
        return self.step

class Cuisine(models.Model):
    cuisine = models.TextField()

    def __str__(self):
        return self.cuisine

class DietType(models.Model):
    diettype = models.TextField()

    def __str__(self):
        return self.diettype

class Recipe(models.Model):
    title = models.TextField(unique=True)
    api_id = models.TextField(unique=True)
    slug = models.TextField(unique=True)
    image_url = models.TextField()
    descreption = models.TextField(unique=True)
    ingredients = models.ManyToManyField(to=Ingredient)
    instructions = models.ManyToManyField(to=Step)
    yields = models.TextField()
    cooking_time = models.TextField()
    cal = models.TextField()
    by = models.TextField()
    tags = models.ManyToManyField(to=Tag)
    diettype = models.ManyToManyField(to=DietType)
    cuisine = models.ManyToManyField(to=Cuisine)

    def __str__(self):
        return self.title

class FeatureImage(models.Model):
    img_url = models.TextField()

    def __str__(self):
        return self.img_url

class BlogPost(models.Model):
    title = models.TextField(unique=True)
    ass_recipe = models.TextField(blank=True)
    img = models.TextField()
    slug = models.SlugField()
    body = models.TextField()
    author = models.TextField()
    categories = models.ManyToManyField(to=Category)
    tags = models.ManyToManyField(to=Tag)
    created = models.DateTimeField(auto_now_add=True)
    show = models.BooleanField(default=False)
