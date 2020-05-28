from django.shortcuts import render
from .models import Article
from shop.models import Category as ShopCategory



# Create your views here.

def article_list(request):
    category_list = ShopCategory.objects.all()
    articles = Article.objects.all().order_by('?')
    return render(request, 'articles/article_list.html', {'articles':articles,'category_list':category_list})

def article_list_latest(request):
    category_list = ShopCategory.objects.all()
    articles = Article.objects.all().order_by('-date')
    return render(request, 'articles/article_list_latest.html', {'articles':articles,'category_list':category_list})

def article_details(request, slug):
    articles = Article.objects.all().exclude(slug=slug).order_by('?')[0:3]
    category_list = ShopCategory.objects.all()
    article = Article.objects.get(slug=slug)
    return render(request, 'articles/article_details.html', {'article':article,'category_list':category_list,'articles':articles})