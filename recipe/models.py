from django.db import models

# Create your models here.

class Tag(models.Model):
    tag = models.TextField(unique=True)

    def __str__(self):
        return self.tag

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
    slug = models.TextField(unique=True)
    image_url = models.TextField()
    descreption = models.TextField(unique=True)
    ingredients = models.ManyToManyField(to=Ingredient)
    instructions = models.ManyToManyField(to=Step)
    yields = models.TextField()
    cooking_time = models.TextField()
    by = models.TextField()
    tags = models.ManyToManyField(to=Tag)
    diettype = models.ManyToManyField(to=DietType)
    cuisine = models.ManyToManyField(to=Cuisine)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.TextField()
    slug = models.SlugField()
    body = models.TextField()
    author = models.TextField()
    tags = models.ManyToManyField()
    show = models.BooleanField(default=False)
