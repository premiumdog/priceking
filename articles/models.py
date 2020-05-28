from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)


    def __str__(self):
        return self.name


class Article(models.Model):
    title= models.CharField(max_length=100)
    slug = models.SlugField(max_length=254, unique=True)
    keywords = models.CharField(max_length=254, blank=True, default="")
    body = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(default='default.png', blank=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE, default="")
    tags = models.ManyToManyField(Tags, related_name='rel_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('article:article_detail', args={self.slug})


class Category(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name



