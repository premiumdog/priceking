from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from . models import Product

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['shop:for_company']
    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.5
    changefreq = 'hourly'
    def items(self):
        return Product.objects.filter(active = True).order_by('id')
    def lastmod(self, obj):
        return obj.created_at
    def location(self, item):
        return reverse('shop:product_details', args=[item.product_id, item.slug])
'''
class ArticleSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    def items(self):
        return Article.objects.all()
    def location(self, item):
        return reverse('shop:article_detail', args=[item.slug])
'''