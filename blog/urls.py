from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomePage"),
    path('category/<str:category>/', views.CategoryView.as_view()),
    path('<str:blog_slug>/', views.BlogView.as_view()),
]