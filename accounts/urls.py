from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/product', views.profile_product, name='profile_product'),
    path('profile/product/<int:pk>/<slug:slug>', views.profile_product_details, name='profile_product_details'),
    path('profile/affilite', views.profile_affiliate, name='profile_affiliate'),
    path('profile/credit', views.profile_credit, name='profile_credit'),
    path('profile/edit/', views.edit_user_profile, name='profile_edit'),
    path('update_list/', views.update_product_list, name='update_product_list'),
    path('check_credit/', views.check_credit, name='check_credit'),
    path('update_xml/', views.update_xml, name='update_xml'),
    path('credit_check/', views.credit_check  , name='credit_check'),
]