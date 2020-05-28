from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,unique=True)
    category_order = models.IntegerField(null=True, blank=True, unique=True)
    category_image = models.ImageField(default='', blank=True, null=True)
    category_banner_link = models.CharField(max_length=254, blank=True, default='', null=True)
    category_banner_img = models.ImageField(null=True, blank=True, default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])



class Product(models.Model):
    product_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=254)
    slug = models.SlugField(null=True, blank=True)
    product_link = models.CharField(max_length=254, blank=True, null=True)
    product_image_link = models.CharField(max_length=254, blank=True, null=True)
    product_price = models.IntegerField(blank=True, null=True)
    product_sale_price = models.IntegerField(blank=True, null=True)
    product_sku = models.CharField(max_length=254, blank=True, null=True)
    product_available = models.CharField(max_length=254, blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    product_category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    product_description = models.TextField(null=True, blank=True)
    product_short_description = models.TextField(null=True, blank=True)
    product_visitor = models.IntegerField(default=1, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    is_offer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])


class Affiliate(models.Model):
    affiliate_product_id = models.PositiveIntegerField()
    affiliate_product_name = models.CharField(max_length=254)
    affiliate_link = models.CharField(max_length=254)
    affiliate_user = models.CharField(max_length=254)
    affiliate_ip_address = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)