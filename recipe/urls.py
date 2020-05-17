from django.urls import path
from . import views

urlpatterns = [
    path("", views.redirector, name='redirect'),
    path("<int:page_no>/", views.index, name="index"),
    path("admin-1/", views.admin_1, name="admin_1"),
    path("blog-admin/", views.blogadmin, name="blog_admin"),
    path("dish/<str:r_name>/", views.recipe, name="recipe"),
    path("contact/", views.contact, name="contact"),
    path("search/", views.search, name="search"),
    path("fetch/", views.fetch, name="fetch"),
    path("pdf/", views.pdfgen, name="pdfgen"),
    path('mealtypes/<str:meal_type>/', views.filter_meals, name="filter_meals"),
    path('cuisine/<str:cuisine>/', views.filter_cuisine, name="filter_cuisine"),
    path('diettype/<str:diettype>/', views.filter_diettype, name="filter_diettype"),
    path("<slug:tag>/", views.tag_search, name="tag_search"),
]
