from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminView.as_view(), name='AdminPage'),
    path('posts/', views.BlogsRecordsView.as_view(), name='BlogRecordsAdmin'),
    path('posts/modify/', views.BlogCreateEditView.as_view(), name='BlogModify'),
    path('logout/', views.logout_view, name="logout"),
]