from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from home.models import Product, Category, Basket, BasketItem

def product_list(request):
    """Display all products with filtering options"""
    products = Product.objects.all()
    categories = Category.objects.all()

    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)

    # Filter by gender
    gender_filter = request.GET.get('gender')
    if gender_filter:
        products = products.filter(gender=gender_filter)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand_name__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_filter,
        'current_gender': gender_filter,
        'search_query': search_query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    """Display individual product details"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_to_basket(request, product_id):
    """Add product to user's basket"""
    product = get_object_or_404(Product, id=product_id)

    # Get or create user's basket
    basket, created = Basket.objects.get_or_create(user=request.user)

    # Get or create basket item
    basket_item, created = BasketItem.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        basket_item.quantity += 1
        basket_item.save()

    messages.success(request, f'{product.name} added to your basket!')
    return redirect('product_detail', slug=product.slug)

@login_required
def basket_view(request):
    """Display user's shopping basket"""
    try:
        basket = Basket.objects.get(user=request.user)
        basket_items = basket.items.all()
        total = sum(item.product.price * item.quantity for item in basket_items)
    except Basket.DoesNotExist:
        basket_items = []
        total = 0

    context = {
        'basket_items': basket_items,
        'total': total,
    }
    return render(request, 'products/basket.html', context)

@login_required
def update_basket_item(request, item_id):
    """Update quantity of basket item"""
    basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
            messages.success(request, 'Basket updated!')
        else:
            basket_item.delete()
            messages.success(request, 'Item removed from basket!')

    return redirect('basket_view')

@login_required
def remove_from_basket(request, item_id):
    """Remove item from basket"""
    basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    product_name = basket_item.product.name
    basket_item.delete()
    messages.success(request, f'{product_name} removed from your basket!')
    return redirect('basket_view')
