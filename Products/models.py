from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import timedelta
from decimal import Decimal
from django.utils.timezone import now
from django.contrib.auth import get_user_model


User = get_user_model()
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active=models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    title = models.CharField(max_length=255)  # Static: Local DB
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    description = models.TextField(blank=True)  # Static: Local DB
    weight=models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Static: Local DB
    is_active = models.BooleanField(default=True)  # Static: Local DB
    is_amazon_product=models.BooleanField(default=False)
    static_price=models.FloatField(null=True, blank=True)
    available_soon = models.BooleanField(default=False)  # Static: Only for manually added
    amazon_id = models.CharField(max_length=100, blank=True, null=True)  # Amazon-specific products
    affiliate_link = models.URLField(blank=True, null=True)  # Amazon-specific products
    is_featured = models.BooleanField(default=False)  # Static: Local DB
    is_best_selling = models.BooleanField(default=False)  # Dynamic: Amazon API
    click_count = models.PositiveIntegerField(default=0)  # Local DB tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='products_created',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='products_updated',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.amazon_id and self.available_soon:
            raise ValueError("The 'available_soon' field can only be set for manually added products.")
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_dynamic_data(self):
        """Fetch dynamic data like price, reviews, stock from API."""
        if not self.amazon_id:
            return {}
        try:
            # Replace with actual API call logic
            data = fetch_product_details_from_amazon_api(self.amazon_id)
            return data
        except Exception as e:
            print(f"Error fetching product data: {e}")
            return {}

    def price(self):
        """Fetch price dynamically."""
        data = self.get_dynamic_data()
        return data.get('price', 'Price not available')

    def stock(self):
        """Fetch stock dynamically."""
        data = self.get_dynamic_data()
        return data.get('stock', 'Stock not available')

    def average_rating(self):
        """Fetch average rating dynamically."""
        data = self.get_dynamic_data()
        return data.get('average_rating', 0)

    def review_count(self):
        """Fetch review count dynamically."""
        data = self.get_dynamic_data()
        return data.get('review_count', 0)

    def get_buy_now_url(self):
        """Get the buy now URL."""
        return self.affiliate_link or f"https://www.amazon.com/dp/{self.amazon_id}"
    
    
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', related_name='wishlisted_by')

    def __str__(self):
        return f"{self.user.email}'s Wishlist"

    def product_count(self):
        """Returns the total number of products in the wishlist."""
        return self.products.count()


