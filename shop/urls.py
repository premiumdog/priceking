from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product/<category_slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('product/<int:pk>/<slug:slug>', views.product_details, name='product_details'),
    path('product/search', views.product_filter, name='search'),
    path('product/latest', views.product_last, name='product_latest'),
    path('product/top', views.product_most_viewed, name='product_most_viewed'),
    path('product/offer', views.product_offer, name='product_offer'),
    path('product/discount', views.product_discount, name='product_discount'),
    path('store/', views.store_list, name='store_list'),
    path('store/<store_slug>/', views.store_details, name='store_details'),
    path('category/', views.category_list, name='category_list'),
    path('product/search/result', views.search_result, name="search_result"),
    path('cegeknek/', views.for_company, name='for_company'),
    path('banner/', views.page_banner, name='page_banner'),
    path('gdpr/', views.page_gdpr, name='page_gdpr'),
    path('aszf/', views.page_aszf, name='page_aszf'),
]