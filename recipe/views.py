from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
import requests, json
from .models import Recipe, Ingredient, Tag, Step, DietType, Cuisine, BlogPost, Category
from django.utils.text import slugify
from pytz import unicode
import random
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import urllib.request
from bs4 import BeautifulSoup
import re, datetime

def admin_1(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_auth = auth.authenticate(username=username, password=password)
        if user_auth is not None:
            if User.is_superuser:
                auth.login(request, user_auth)
                context = {
                    'username': username
                }
        else:
            context = {
                'message': 'Either Wrong credentials or not a superuser'
            }
        return render(request, "admin-1/index.html", context)
    else:
        if request.user.is_authenticated and request.user.is_superuser:
            context = {
                    'username': request.user.username
                }
            return render(request, "admin-1/index.html", context)
        else:
            print("here")
            return render(request, 'admin-1/login.html')

def logout(request):
    auth.logout(request)   
    return redirect('/admin-1')

def all_posts(request):
    all_blogs = BlogPost.objects.all()
    context = {
        'username': request.user.username,
        'all_blogs': all_blogs,
    }
    return render(request, "admin-1/data-table.html", context)

def create_blog(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        categories = Category.objects.all()
        context = {
            'tags': tags,
            'categories': categories,
        }
        return render(request, "blog/createblog.html", context)

    else:
        title = request.POST['title']
        featimgurl = request.POST['imgurl']
        body = request.POST['body']
        author = request.POST['author']
        tags = request.POST.getlist('tag')
        categories = request.POST.getlist('category')
        option = request.POST['option']
        rand_blog = list(BlogPost.objects.all())
        try:
            try:
                random_items = random.sample(rand_blog, 3)
            except:
                random_items = random.sample(rand_blog, Recipe.objects.count())
        except:
            random_items = []
        context = {
            "title": title,
            "imgurl": featimgurl,
            "body": body,
            "date": datetime.datetime.now(),
            "author": author,
            "tags": tags,
            "categories": categories,
            "rand_blog": list(random_items)
        }
        if option == "preview":
            return render(request, "blog/blogpost.html", context)
        else:
            BlogPost.objects.create(title=title, img=featimgurl, slug=slugify(unicode(title)), body=body, author=author)
            blg_inst = BlogPost.objects.get(title=title)
            for tag in tags:
                blg_inst.tags.add(tag)
            for category in categories:
                blg_inst.categories.add(category)
            return redirect("/admin-1/all-posts/")

def youtube_links(quer):
    textToSearch = quer
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    no = 0
    l = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if no > 2:
            break
        no += 1
        vid['href'] = vid['href'].replace("watch?v=", "embed/")
        l.append('https://www.youtube.com/' + vid['href'])
    return l

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def pdfgen(request):
    if request.method == "POST":
        title = request.POST['title']
        r_inst = Recipe.objects.get(title=title)
        ingredients = r_inst.ingredients
        steps = r_inst.instructions
        context = {
            'title': title,
            'ingredients': ingredients,
            'steps': steps
        }
        pdf = render_to_pdf('recipe/recipepdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

def fetch(request):
    if request.method == "POST":
        secret_key = request.POST["username"]
        no_of_posts = request.POST["number"]
        if secret_key == "tejas":
            params = {
                'apiKey': '98756d2aa51b45ad86ebac98e8bda863',
            }

            headers = {
                'Content-Type': 'application/json'
            }

            for i in  range(0, int(no_of_posts)):
                random_recipe = requests.get("https://api.spoonacular.com/recipes/random", params=params, headers=headers)
                random_recipe = json.loads(random_recipe.text)
                title = random_recipe['recipes'][0]['title']
                api_id = random_recipe['recipes'][0]['id']
                try:
                    image_url = random_recipe['recipes'][0]['image']
                except:
                    image_url = "https://via.placeholder.com/300x160"
                descreption = random_recipe['recipes'][0]['summary']
                try:
                    cal = re.search("[0-9]* calories", descreption).group(0)
                except:
                    cal = ""
                try:
                    instructions = random_recipe['recipes'][0]['analyzedInstructions'][0]['steps']
                except:
                    instructions = []
                steps_list = []
                for i in instructions:
                    steps_list.append(i['step'])
                yields = random_recipe['recipes'][0]['servings']
                cooking_time = random_recipe['recipes'][0]['readyInMinutes']
                ingredients = random_recipe['recipes'][0]['extendedIngredients']
                ingredient_list = []
                for ingredient in ingredients:
                    ingredient_list.append(ingredient['originalString'])
                by = random_recipe['recipes'][0]['sourceName']
                tags = random_recipe['recipes'][0]['dishTypes']
                diettypes = random_recipe['recipes'][0]['diets']
                cuisines = random_recipe['recipes'][0]['cuisines']

                slug = slugify(unicode(title))

                try:
                    Recipe.objects.create(title=title, image_url=image_url, descreption=descreption, yields=yields, cooking_time=cooking_time, by=by, slug=slug, cal=cal, api_id=api_id)

                    recipe_instance = Recipe.objects.get(title=title)

                    for _ in ingredient_list:
                        try:
                            ing = Ingredient.objects.get(ingredient=_)
                        except:
                            Ingredient.objects.create(ingredient=_)
                            ing = Ingredient.objects.get(ingredient=_)
                        recipe_instance.ingredients.add(ing)

                    for _ in tags:
                        _ = slugify(unicode(_))
                        try:
                            tag = Tag.objects.get(tag=_)
                        except:
                            Tag.objects.create(tag=_)
                            tag = Tag.objects.get(tag=_)
                        recipe_instance.tags.add(tag)
                    
                    for _ in diettypes:
                        _ = slugify(unicode(_))
                        try:
                            diettype = DietType.objects.get(diettype=_)
                        except:
                            DietType.objects.create(diettype=_)
                            diettype = DietType.objects.get(diettype=_)
                        recipe_instance.diettype.add(diettype)
                    
                    for _ in cuisines:
                        _ = slugify(unicode(_))
                        try:
                            cuisine = Cuisine.objects.get(cuisine=_)
                        except:
                            Cuisine.objects.create(cuisine=_)
                            cuisine = Cuisine.objects.get(cuisine=_)
                        recipe_instance.cuisine.add(cuisine)


                    for _ in steps_list:
                        try:
                            step = Step.objects.get(step=_)
                        except:
                            Step.objects.create(step=_)
                            step = Step.objects.get(step=_)
                        recipe_instance.instructions.add(step)
                except:
                    pass

        context = {
            'message': '{} recipes successfully added'.format(str(no_of_posts))
        }
        return render(request, "recipe/fetch.html", context)
    
    else:
        return render(request, "recipe/fetch.html")

def index(request, page_no):
    queryset = Recipe.objects.all().reverse()
    p = Paginator(queryset, 6)
    li = list(p.page_range)
    queryset = p.page(page_no).object_list
    tags_qset = Tag.objects.all()
    cuisine = Cuisine.objects.all()
    diettypes = DietType.objects.all()
    nxt_pg = page_no + 1
    prv_pg = page_no - 1
    if nxt_pg > li[-1]:
        nxt_pg = page_no
    if prv_pg < 1:
        prv_pg = 1
    rand_blog = list(BlogPost.objects.all())
    try:
        try:
            random_items = random.sample(rand_blog, 4)
        except:
            random_items = random.sample(rand_blog, Recipe.objects.all().count())
    except:
        random_items = []
    context = {
        'all_recipes': queryset,
        'tags': tags_qset,
        'cuisine': cuisine,
        'dietypes': diettypes,
        'var_title': 'Recipes',
        'next': nxt_pg,
        'prev': prv_pg,
        'rand_blog': list(random_items)
    }

    return render(request, 'recipe/index.html', context)

def index1(request):
    page_no = 1
    queryset = Recipe.objects.all().reverse()
    p = Paginator(queryset, 6)
    li = list(p.page_range)
    queryset = p.page(page_no).object_list
    tags_qset = Tag.objects.all()
    cuisine = Cuisine.objects.all()
    diettypes = DietType.objects.all()
    nxt_pg = page_no + 1
    prv_pg = page_no - 1
    if nxt_pg > li[-1]:
        nxt_pg = page_no
    if prv_pg < 1:
        prv_pg = 1
    rand_blog = list(BlogPost.objects.all())
    try:
        try:
            random_items = random.sample(rand_blog, 4)
        except:
            random_items = random.sample(rand_blog, BlogPost.objects.all().count())
    except:
        random_items = []

    context = {
        'all_recipes': queryset,
        'tags': tags_qset,
        'cuisine': cuisine,
        'dietypes': diettypes,
        'var_title': 'Recipes',
        'next': nxt_pg,
        'prev': prv_pg,
        'rand_blog': list(random_items)
    }

    return render(request, 'recipe/index.html', context)

def recipe(request, r_name):
    queryset = Recipe.objects.get(slug=r_name)
    recipe_qset = list(Recipe.objects.all())
    try:
        random_items = random.sample(recipe_qset, 4)
    except:
        random_items = random.sample(recipe_qset, Recipe.objects.count())
    context = {
        'recommended': list(random_items),
        'recipe': queryset,
        'links': youtube_links(queryset.title),
    }
    return render(request, 'recipe/recipe.html', context)

def contact(request):
    return render(request, "recipe/contact.html")

offset = 0
def filter_meals(request, meal_type):
    global offset
    offset += 3
    if offset > 899:
        offset = 1

    param = {
        'apiKey': '98756d2aa51b45ad86ebac98e8bda863',
        'type': meal_type,
        'offset': offset,
        'number': 3
    }
    headers = {
        'Content-Type': 'application/json'
    }
    recipes = requests.get("https://api.spoonacular.com/recipes/complexSearch".format(meal_type, offset), params=param, headers=headers)
    recipe_obj_list = json.loads(recipes.text)
    recipe_list = recipe_obj_list['results']
    recipe_id_list = []
    for recipe_id in recipe_list:
        recipe_id_list.append(recipe_id['id'])

    query_list = []

    params = {
        'apiKey': '98756d2aa51b45ad86ebac98e8bda863',
    }

    headers = {
        'Content-Type': 'application/json'
    }

    for rec_id in recipe_id_list:
        random_recipe = json.loads(requests.get("https://api.spoonacular.com/recipes/{}/information".format(rec_id), params=params, headers=headers).text)
        api_id = random_recipe['id']
        try:
            title = random_recipe['title']
        except:
            title = ""
        try:
            image_url = random_recipe['image']
        except:
            image_url = "https://via.placeholder.com/300x160"
        try:
            descreption = random_recipe['summary']
        except:
            descreption = ""
        try:
            cal = re.search("[0-9]* calories", descreption).group(0)
        except:
            cal = ""
        try:
            instructions = random_recipe['analyzedInstructions'][0]['steps']
        except:
            instructions = []
        steps_list = []
        for i in instructions:
            steps_list.append(i['step'])
        yields = random_recipe['servings']
        cooking_time = random_recipe['readyInMinutes']
        ingredients = random_recipe['extendedIngredients']
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append(ingredient['originalString'])
        by = random_recipe['sourceName']
        tags = random_recipe['dishTypes']
        diettypes = random_recipe['diets']
        cuisines = random_recipe['cuisines']

        slug = slugify(unicode(title))

        if Recipe.objects.filter(title=title).exists():
            r = Recipe.objects.get(title=title)
            query_list.append(r)
        
        else:
            Recipe.objects.create(title=title, image_url=image_url, descreption=descreption, yields=yields, cooking_time=cooking_time, by=by, slug=slug, cal=cal, api_id=api_id)
            recipe_instance = Recipe.objects.get(title=title)

            for _ in ingredient_list:
                try:
                    ing = Ingredient.objects.get(ingredient=_)
                except:
                    Ingredient.objects.create(ingredient=_)
                    ing = Ingredient.objects.get(ingredient=_)
                recipe_instance.ingredients.add(ing)

            for _ in tags:
                _ = slugify(unicode(_))
                try:
                    tag = Tag.objects.get(tag=_)
                except:
                    Tag.objects.create(tag=_)
                    tag = Tag.objects.get(tag=_)
                recipe_instance.tags.add(tag)

            for _ in diettypes:
                _ = slugify(unicode(_))
                try:
                    diettype = DietType.objects.get(diettype=_)
                except:
                    DietType.objects.create(diettype=_)
                    diettype = DietType.objects.get(diettype=_)
                recipe_instance.diettype.add(diettype)
            
            for _ in cuisines:
                _ = slugify(unicode(_))
                try:
                    cuisine = Cuisine.objects.get(cuisine=_)
                except:
                    Cuisine.objects.create(cuisine=_)
                    cuisine = Cuisine.objects.get(cuisine=_)
                recipe_instance.cuisine.add(cuisine)

            for _ in steps_list:
                try:
                    step = Step.objects.get(step=_)
                except:
                    Step.objects.create(step=_)
                    step = Step.objects.get(step=_)
                recipe_instance.instructions.add(step)
            r = Recipe.objects.get(title=title)
            query_list.append(r)

    queryset = query_list
    tags_qset = Tag.objects.all()
    cuisine = Cuisine.objects.all()
    diettypes = DietType.objects.all()

    context = {
        'all_recipes': queryset,
        'tags': tags_qset,
        'cuisine': cuisine,
        'dietypes': diettypes,
        'var_title': '{}'.format(meal_type + " recipes")
    }

    return render(request, 'recipe/index.html', context)

def filter_diettype(request, diettype, page_no):
    queryset = Recipe.objects.filter(diettype__diettype=diettype)
    tags_qset = Tag.objects.all()
    cuisine = Cuisine.objects.all()
    diettypes = DietType.objects.all()
    p = Paginator(queryset, 6)
    queryset = p.page(page_no).object_list
    li = list(p.page_range)
    nxt_pg = page_no + 1
    prv_pg = page_no - 1
    if nxt_pg > li[-1]:
        nxt_pg = page_no
    if prv_pg < 1:
        prv_pg = 1
    context = {
        'all_recipes': queryset,
        'tags': tags_qset,
        'cuisine': cuisine,
        'dietypes': diettypes,
        'var_title': '{}'.format(diettype + " recipes"),
        'next': "diettype/" + diettype + "/" + str(nxt_pg),
        'prev': "diettype/" + diettype + "/" + str(prv_pg)
    }
    return render(request, 'recipe/index.html', context)

def filter_cuisine(request, cuisine):
    c = cuisine
    queryset = Recipe.objects.filter(cuisine__cuisine=cuisine)
    tags_qset = Tag.objects.all()
    cuisine = Cuisine.objects.all()
    diettypes = DietType.objects.all()
    context = {
        'all_recipes': queryset,
        'tags': tags_qset,
        'cuisine': cuisine,
        'dietypes': diettypes,
        'var_title': '{}'.format(c + " recipes")
    }
    return render(request, 'recipe/index.html', context)

def search(request):
    flag = False
    query = request.POST['query']

    if Recipe.objects.filter(title__contains=query):
        flag = True
        query_list = Recipe.objects.filter(title__contains=query) 
    
    if flag == False:

        params = {
            'apiKey': '98756d2aa51b45ad86ebac98e8bda863',
            'query': query,
            'number': '12',
        }
        headers = {
            'Content-Type': 'application/json'
        }
        recipe_obj_list = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=params, headers=headers)
        recipe_obj_list = json.loads(recipe_obj_list.text)
        recipe_list = recipe_obj_list['results']
        recipe_id_list = []
        for recipe_id in recipe_list:
            recipe_id_list.append(recipe_id['id'])

        query_list = []

        params = {
            'apiKey': '98756d2aa51b45ad86ebac98e8bda863',
        }

        for rec_id in recipe_id_list:
            random_recipe = json.loads(requests.get("https://api.spoonacular.com/recipes/{}/information".format(rec_id), params=params, headers=headers).text)
            api_id = random_recipe['id']
            try:
                title = random_recipe['title']
            except:
                title = "API Failed"
            
            try:
                image_url = random_recipe['image']
            except:
                image_url = "https://via.placeholder.com/300x190"
            
            try:
                descreption = random_recipe['summary']
            except:
                descreption = ""
            try:
                cal = re.search("[0-9]* calories", descreption).group(0)
            except:
                cal = ""
            try:
                instructions = random_recipe['analyzedInstructions'][0]['steps']
            except:
                instructions = []
            steps_list = []
            for i in instructions:
                steps_list.append(i['step'])
            yields = random_recipe['servings']
            cooking_time = random_recipe['readyInMinutes']
            ingredients = random_recipe['extendedIngredients']
            ingredient_list = []
            for ingredient in ingredients:
                ingredient_list.append(ingredient['originalString'])
            by = random_recipe['sourceName']
            tags = random_recipe['dishTypes']
            diettypes = random_recipe['diets']
            cuisines = random_recipe['cuisines']

            slug = slugify(unicode(title))

            if Recipe.objects.filter(title=title).exists():
                r = Recipe.objects.get(title=title)
                query_list.append(r)
            
            else:
                try:
                    Recipe.objects.create(title=title, image_url=image_url, descreption=descreption, yields=yields, cooking_time=cooking_time, by=by, slug=slug, cal=cal, api_id=api_id)
                    recipe_instance = Recipe.objects.get(title=title)

                    for _ in ingredient_list:
                        try:
                            ing = Ingredient.objects.get(ingredient=_)
                        except:
                            Ingredient.objects.create(ingredient=_)
                            ing = Ingredient.objects.get(ingredient=_)
                        recipe_instance.ingredients.add(ing)

                    for _ in tags:
                        _ = slugify(unicode(_))
                        try:
                            tag = Tag.objects.get(tag=_)
                        except:
                            Tag.objects.create(tag=_)
                            tag = Tag.objects.get(tag=_)
                        recipe_instance.tags.add(tag)

                    for _ in diettypes:
                        _ = slugify(unicode(_))
                        try:
                            diettype = DietType.objects.get(diettype=_)
                        except:
                            DietType.objects.create(diettype=_)
                            diettype = DietType.objects.get(diettype=_)
                        recipe_instance.diettype.add(diettype)
                    
                    for _ in cuisines:
                        _ = slugify(unicode(_))
                        try:
                            cuisine = Cuisine.objects.get(cuisine=_)
                        except:
                            Cuisine.objects.create(cuisine=_)
                            cuisine = Cuisine.objects.get(cuisine=_)
                        recipe_instance.cuisine.add(cuisine)

                    for _ in steps_list:
                        try:
                            step = Step.objects.get(step=_)
                        except:
                            Step.objects.create(step=_)
                            step = Step.objects.get(step=_)
                        recipe_instance.instructions.add(step)
                    r = Recipe.objects.get(title=title)
                    query_list.append(r)
                except:
                    pass

    queryset = query_list
    tags_qset = Tag.objects.all()
    cuisine = Cuisine.objects.all()
    diettypes = DietType.objects.all()

    context = {
        'all_recipes': queryset,
        'tags': tags_qset,
        'cuisine': cuisine,
        'dietypes': diettypes,
        'var_title': '{}'.format(query + " recipes")
    }

    return render(request, 'recipe/index.html', context)

def tag_search(request, tag, page_no):
    queryset = Recipe.objects.filter(tags__tag=slugify(unicode(tag)))
    tags_qset = Tag.objects.all()
    cuisine = Cuisine.objects.all()
    diettypes = DietType.objects.all()
    p = Paginator(queryset, 6)
    queryset = p.page(page_no).object_list
    li = list(p.page_range)
    nxt_pg = page_no + 1
    prv_pg = page_no - 1
    if nxt_pg > li[-1]:
        nxt_pg = page_no
    if prv_pg < 1:
        prv_pg = 1

    context = {
        'all_recipes': queryset,
        'tags': tags_qset,
        'cuisine': cuisine,
        'dietypes': diettypes,
        'var_title': '{}'.format(tag + " recipes"),
        'next': tag + "/" + str(nxt_pg),
        'prev': tag + "/" + str(prv_pg)
    }
    return render(request, 'recipe/index.html', context)

def editblog(request, blg_name):
    if request.method == "GET":
        tags = Tag.objects.all()
        categories = Category.objects.all()
        blg_inst = BlogPost.objects.get(slug=blg_name)
        context = {
            'title': blg_inst.title,
            'imgurl': blg_inst.img,
            'body': blg_inst.body,
            'author': blg_inst.author,
            'tags': tags,
            'categories': categories,
            'slug': blg_inst.slug,
        }
        return render(request, "blog/editblog.html", context)

    else:
        title = request.POST['title']
        featimgurl = request.POST['imgurl']
        body = request.POST['body']
        author = request.POST['author']
        tags = request.POST.getlist('tag')
        categories = request.POST.getlist('category')
        option = request.POST['option']
        rand_blog = list(BlogPost.objects.all())
        try:
            try:
                random_items = random.sample(rand_blog, 3)
            except:
                random_items = random.sample(rand_blog, Recipe.objects.count())
        except:
            random_items = []
        context = {
            "title": title,
            "imgurl": featimgurl,
            "body": body,
            "date": datetime.datetime.now(),
            "author": author,
            "tags": tags,
            "categories": categories,
            "rand_blog": list(random_items)
        }
        if option == "preview":
            return render(request, "blog/blogpost.html", context)
        else:
            blg_inst = BlogPost.objects.get(slug=blg_name)
            blg_inst.title = title
            blg_inst.img = featimgurl
            blg_inst.body = body
            blg_inst.date = datetime.datetime.now()
            blg_inst.author = author
            for tag in tags:
                blg_inst.tags.add(tag)
            for category in categories:
                blg_inst.categories.add(category)
            blg_inst.save()
            return redirect("/admin-1/all-posts/")

def renderblog(request, blg_name):
    blg_inst = BlogPost.objects.get(slug=blg_name)
    rand_blog = list(BlogPost.objects.all())
    try:
        random_items = random.sample(rand_blog, 8)
    except:
        random_items = random.sample(rand_blog, BlogPost.objects.all().count())
        
    tags = [i for i in blg_inst.tags.all()]
    context = {
            "slug": blg_inst.slug,
            "title": blg_inst.title,
            "imgurl": blg_inst.img,
            "body": blg_inst.body,
            "date": blg_inst.created,
            "author": blg_inst.author,
            "tags": tags,
            "categories": blg_inst.categories,
            "rand_blog": list(random_items)
    }
    return render(request, "blog/blogpost.html", context)