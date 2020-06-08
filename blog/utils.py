from django.db.models import Q
from random import randint
from . import models
from newspaper import Article
import requests
from bs4 import BeautifulSoup

class Utils(object):

    def search(self, query):
        queries = query.split(" ")
        queryset = []
        for q in queries:
            posts = models.BlogPost.objects.filter(
                Q(title__contains=str(q)) | 
                Q(body__contains=str(q)) |
                Q(meta_descreption__contains=str(q))
            ).distinct()
            for post in posts:
                queryset.append(post)
        
        return list(set(queryset))


    # Common Queries for almost all pages
    def homepage_cotent_queries(self):
        trending_blogs = []
        try:
            trending_blogs = models.BlogPost.objects.all().filter(publisheded=True).order_by('-id')[:6]
        except:
            trending_blogs = models.BlogPost.objects.all().filter(published=True).order_by('-id')[:models.BlogPost.objects.all().count()]
        random_blogs = []
        try:
            random_blogs = models.BlogPost.objects.filter(published=True).order_by('?')[:3]
        except:
            random_blogs = models.BlogPost.objects.filter(published=True).order_by('?')[:models.BlogPost.objects.all().count()]
        random_title_only_blogs = []
        try:
            random_title_only_blogs = models.BlogPost.objects.filter(published=True).order_by('?')[:3]
        except:
            random_title_only_blogs = models.BlogPost.objects.filter(published=True).values('title').order_by('?')[:models.BlogPost.objects.all().count()]
        categories = models.Category.objects.all()
        return {
            'trending_blogs': trending_blogs[:3],
            'random_blogs': random_blogs,
            'random_title_only_blogs': random_title_only_blogs,
            'categories': categories,
            'main_blog': trending_blogs[0],
            'featured': trending_blogs
        }


    def email_saver(self, email):
        if email and not models.Email.objects.filter(email=email).exists():
                models.Email.objects.create(email=email)
        return models.Email.objects.get(email=email)


    def category_filter(self, category_pk):
        category_filtered = models.BlogPost.objects.filter(category__in=[category_pk])
        return {
            'filtered': category_filtered
        }


    def blog_page_content_queries(self, blog_slug):

        blog_obj = models.BlogPost.objects.get(slug=blog_slug)
        keyword_list = [keyword.pk for keyword in blog_obj.keywords.all()]
        keyword_match_blogs = models.BlogPost.objects.filter(keywords__in=keyword_list)[:3]
        return {
            'blog': blog_obj,
            'similar_posts': keyword_match_blogs,
            'extras': self.homepage_cotent_queries(),
        }


    def comment_saver(self, name, email, comment):

        email_obj = self.email_saver(email)
        comment_obj = models.Comment.objects.create(name=name, comment=comment)
        comment_obj.email.add(email_obj)


    def gen_post(self, website):
        
        article = Article(website)
        article.download()
        article.parse()
        article.nlp()
        body = {
            'email': 'vetron.marketing@gmail.com',
            'pass': 'Vetron1234.',
            's': article.text,
            'quality': 'readable',
            'returnspin': 'true',
            'nonested': 'on',
        }
        r = requests.post('http://wordai.com/users/turing-api.php', data=body)
        return {
            'title': article.title,
            'body': r.text,
            'feature_img': article.top_image,
            'video_links': article.movies,
            'authors': article.authors,
            'meta': article.summary[:155],
            'keywords': article.keywords,
            'images': article.images,
        }
