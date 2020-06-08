from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from recipe.models import Recipe
from . import models
import json
from .utils import Utils
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.text import slugify


class HomeView(View, Utils):

    def get(self, request):
        query = request.GET.get('query', None)
        if query:
            context = {
                'query': query,
                'posts': super().search(query),
                'extras': super().homepage_cotent_queries(),
            }
            return render(request, 'blog/category-list.html', context)
        return render(request, 'blog/index08.html', context=super().homepage_cotent_queries())
    
    def post(self, request):
        email = request.POST.get('email', None)
        super().email_saver(email)
        return redirect('/blog')


class CategoryView(View, Utils):


    def get(self, request, category):
        context = {
            'category_obj': models.Category.objects.get(category=category),
            'category': category,
            'category_filtered': super().category_filter(models.Category.objects.get(category=category).pk),
            'extras': super().homepage_cotent_queries()
        }
        return render(request, 'blog/category-grid.html', context)

    def post(self, request, category):

        email = request.POST.get('email', None)
        super().email_saver(email)
        return redirect('/blog/category/{}'.format(category))


class BlogView(View, Utils):

    def get(self, request, blog_slug):
        return render(request, 'blog/post-details.html', super().blog_page_content_queries(blog_slug))
    
    def post(self, request, blog_slug):
        try:
            r_username = request.POST['r_username']
            r_email = request.POST.get('r_email', None)
            r_password = request.POST.get('r_password', None)
            if r_email != None and r_password != None and r_username != None:
                super().email_saver(r_email)
                user = User.objects.create_user(username=r_username, email=r_email, password=r_password)

            l_username = request.POST.get('l_username', None)
            l_password = request.POST.get('l_password', None)
            if l_username != None and l_password != None:
                user = authenticate(request, username=l_username, password=l_password)
                if user != None:
                    login(request, user)

            comment = request.POST.get('message', None)
            if comment != None:
                cmnt_obj = models.Comment.objects.create(comment=comment)
                cmnt_obj.user.add(request.user)
                models.BlogPost.objects.get(slug=blog_slug).comments.add(cmnt_obj)
            
            return redirect('/blog/{}/'.format(blog_slug))
        except:
            share_count = int(json.loads(request.body)['share_count'])
            blog_obj = models.BlogPost.objects.get(slug=blog_slug)
            blog_obj.shares = share_count
            blog_obj.save()
            return HttpResponse(json.dumps({'shares': share_count}), content_type='application/json')


class AdminView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'admin-1/index.html', {'username': request.user.username})
        return render(request, 'admin-1/login.html')

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username != None and password != None:
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
            return redirect('/blog/admin/')


class BlogsRecordsView(View):

    def get(self, request):
        title = request.GET.get('title', None)
        if title != None and request.user.is_authenticated:
            models.BlogPost.objects.get(title=title).delete()
            return redirect('/blog/admin/posts/')
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
        if title != None and request.user.is_authenticated:
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
            if published == "on":
                published = True
            else:
                published = False
            blog_obj = models.BlogPost.objects.create(title=title, meta_descreption=meta_descreption, feat_img=feat_img, body=body, author=author, time_to_read=time_to_read, slug=slug, published=published)
            for keyword in keywords:
                blog_obj.keywords.add(keyword)
            for category in category:
                blog_obj.category.add(category)
            if changer == "preview":
                return render(request, 'blog/post-details.html', super().blog_page_content_queries(blog_obj.title))
            elif changer == "post":
                return redirect('/blog/admin/posts/')
        except:
            spinnedarticle = super().gen_post(json.loads(request.body)['tp_blog_link'])
            spinnedarticle['images'] = list(spinnedarticle['images'])
            return HttpResponse(json.dumps(spinnedarticle), content_type='application/json')
