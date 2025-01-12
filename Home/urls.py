from django.urls import  path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from  . import views
from Products .views import *
urlpatterns = [
path('',index,name='home'),

path('search_suggestions/', search_suggestions, name='search_suggestions'),
path('search/', search_products_home, name='search_products'),
path('accounts/login/', custom_login_view, name='login'),
path('logout/',custom_logout,name='logout'),
path('register/', register, name='register'),
path('profile/', profile_view, name='profile'),

]