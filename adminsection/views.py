from django.shortcuts import render
from blog import models
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from recipe.models import Recipe
import json
from blog.utils import Utils
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.text import slugify
from django.db.models import Q

# Create your views here.

class AdminView(View):
    
    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'admin-1/index.html', {'username': request.user.username})
        return render(request, 'admin-1/login.html')

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username != None and password != None:
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
            return redirect('/user/admin/')


class BlogsRecordsView(View):

    def get(self, request):
        title = request.GET.get('title', None)
        if title != None and request.user.is_superuser:
            models.BlogPost.objects.get(title=title).delete()
            return redirect('/user/admin/posts/')
        context = {
            'username': request.user.username,
            'blogs': models.BlogPost.objects.all(),
        }
        return render(request, 'admin-1/data-table.html', context)


class BlogCreateEditView(View, Utils):

    def get(self, request):
        title = request.GET.get('title')
        context = {
                'categories': models.Category.objects.all(),
                'keywords': models.KeyWord.objects.all(),
                'username': request.user.username,
            }
        if title != None and request.user.is_superuser:
            blog_obj = models.BlogPost.objects.get(title=title)
            context['blog'] = blog_obj
        return render(request, 'admin-1/createblog.html', context)

    def post(self, request):
        try:
            changer = request.POST["changer"]
            title = request.POST.get("title", None)
            try:
                models.BlogPost.objects.get(title=title).delete()
            except:
                pass
            slug = slugify(title)
            meta_descreption = request.POST.get("meta_descreption", None)
            feat_img = request.POST.get("feat_img", None)
            body = request.POST.get("body", None)
            author = request.POST.get("author", None)
            keywords = request.POST.getlist("keywords")
            category = request.POST.getlist("category")
            time_to_read = request.POST.get("time_to_read", None)
            published = request.POST.get("published", None)
            recipe_show = request.POST.get("recipe", None)
            if recipe_show != None:
                recipe_inst = Recipe.objects.filter(Q(title__contains=recipe_show) | Q(descreption__contains=recipe_show))[0]
            if published == "on":
                published = True
            else:
                published = False
            blog_obj = models.BlogPost.objects.create(title=title, meta_descreption=meta_descreption, feat_img=feat_img, body=body, author=author, time_to_read=time_to_read, slug=slug, published=published)
            if recipe_inst != None:
                blog_obj.recipe.add(recipe_inst)
            for keyword in keywords:
                blog_obj.keywords.add(keyword)
            for category in category:
                blog_obj.category.add(category)
            if changer == "preview":
                return render(request, 'blog/post-details.html', super().blog_page_content_queries(blog_obj.slug))
            elif changer == "post":
                return redirect('/user/admin/posts/')
        except:
            spinnedarticle = super().gen_post(json.loads(request.body)['tp_blog_link'])
            spinnedarticle['images'] = list(spinnedarticle['images'])
            return HttpResponse(json.dumps(spinnedarticle), content_type='application/json')

def logout_view(request):
    logout(request)
    return redirect('/user/admin/')