from django.urls import  path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    
 path('product_detail/<slug:slug>/', product_detail, name='product_detail'), 
 path('wishlist/', wishlist, name='wishlist'), 
    path('add-to-wishlist/<slug:product_slug>/',add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<slug:product_slug>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('view-products/<slug:category_slug>/',list_products,name='view-products')
  

    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)