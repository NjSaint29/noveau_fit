from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    """View to render the index page."""
    # Get featured products (first 8 products)
    featured_products = Product.objects.all()[:8]

    context = {
        'featured_products': featured_products,
    }

    return render(request, 'home/index.html', context)