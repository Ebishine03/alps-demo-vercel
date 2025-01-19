from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404, render
from .models import Product,Wishlist,Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Subquery, OuterRef

from django.utils.timezone import now
from django.db.models.functions import Coalesce
from django.db.models import Q, Min, Case, When, F, FloatField,Value,BooleanField
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from itertools import islice
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.utils import timezone
import uuid
def chunked(iterable, size):
    it = iter(iterable)
    return iter(lambda: list(islice(it, size)), [])
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Product, Category
from django.utils import timezone
def list_products(request, category_slug):
    search_query = request.GET.get('search-query', '')
    sort_by = request.GET.get('sort-by', 'default')
    page = request.GET.get('page', 1)  # Get the current page number from the query parameters

    if category_slug == 'featured_products':
        products = Product.objects.filter(is_active=True, is_featured=True)
        title = "Featured Products"
    elif category_slug == 'best_selling':
        products = Product.objects.filter(is_active=True).order_by('-sales')[:10]
        title = "Best Selling Products"
    else:
        # Regular category filter
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_active=True)
        title = category.name

    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    def fetch_product_price(product):
        if product.is_amazon_product:
            return fetch_amazon_data(product.amazon_id).get('price', float('inf'))
        return product.price

    def fetch_product_rating(product):
        if product.is_amazon_product:
            return fetch_amazon_data(product.amazon_id).get('rating', 0)
        return 0

    # Sorting logic
    if sort_by == 'price_low_to_high':
        products = sorted(products, key=fetch_product_price)
    elif sort_by == 'price_high_to_low':
        products = sorted(products, key=fetch_product_price, reverse=True)
    elif sort_by == 'rating':
        products = sorted(
            products,
            key=lambda p: fetch_product_rating(p),
            reverse=True
        )
    elif sort_by == 'date_newest':
        products = products.order_by('-created_at')
    elif sort_by == 'date_oldest':
        products = products.order_by('created_at')
    elif sort_by == 'name_asc':
        products = products.order_by('title')
    elif sort_by == 'name_desc':
        products = products.order_by('-title')
    
    # Pagination
    paginator = Paginator(products,10)  
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'products': paginated_products,
        'title': title,
        'category_slug': category_slug,
        'paginator': paginator,
        'sort_by': sort_by,
        'category':category.name   }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/partial_product.html', {'products': paginated_products})
        return JsonResponse({'html': html})

    return render(request, 'products/view-products.html', context)
def product_detail(request,slug):
    
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True  
    ).exclude(id=product.id)[:4]  

    context = {
        'product': product,
        'related_products':related_products
    }
    
    return render(request, 'products/product_details.html', context)
@login_required
def wishlist(request):

    wishlist = Wishlist.objects.filter(user=request.user).first()
    print(wishlist)
    wishlist_items = wishlist.products.all() if wishlist else []
  
   
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'products/wishlist.html', context)
@login_required
def add_to_wishlist(request, product_slug):
  

  
    product = get_object_or_404(Product, slug=product_slug)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    print(product,wishlist)
    if not wishlist.products.filter(id=product.id).exists():
        wishlist.products.add(product)
        wishlist.save()
        print(f"Product '{product.title}' added to {request.user}'s wishlist.")
    else:
        print(f"Product '{product.title}' is already in {request.user}'s wishlist.")

    return redirect('wishlist')  
        


@login_required
def remove_from_wishlist(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)

    # Get the wishlist item for the user
    wishlist_item = Wishlist.objects.filter(user=request.user).first()

    if wishlist_item and product in wishlist_item.products.all():
        wishlist_item.products.remove(product)  

    return redirect('wishlist') 