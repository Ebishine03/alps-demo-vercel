from Products.models import Category,Wishlist



def category_context(request):
    categories = Category.objects.filter(is_active=True).values('name', 'slug')
    print(categories)
    return {'global_categories': categories}
def wishlist_count(request):
    
    if request.user.is_authenticated:
        try: 
            wishlist = Wishlist.objects.get(user=request.user) 
            count = wishlist.product_count() 
        except Wishlist.DoesNotExist: count = 0 
    else: 
       count = 0
    return {'wishlist_count':count}