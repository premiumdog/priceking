from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('', views.article_list, name="article_list"),
    path('latest/', views.article_list_latest, name="article_list_latest"),
    path('<slug:slug>/', views.article_details, name='article_detail'),
]