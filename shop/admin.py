from django.contrib import admin
from shop.models import Product, Affiliate, Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category_order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['category_order']
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_id', 'product_name','slug', 'product_price','product_sale_price','product_category','active','is_offer', 'user','created_at','updated_at']
    list_editable = ['active', 'product_category','is_offer']

class AffiliateAdmin(admin.ModelAdmin):
    list_display = ['id', 'affiliate_product_id', 'affiliate_product_name', 'affiliate_link','affiliate_user','affiliate_ip_address','created_at']


admin.site.register(Product, ProductAdmin)
admin.site.register(Affiliate, AffiliateAdmin)