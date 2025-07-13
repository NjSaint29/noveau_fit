from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import Order, WishList, WishListItem, Product

@login_required
def profile_view(request):
    """Display user profile with order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'products/profile.html', context)

@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    try:
        wishlist = WishList.objects.get(user=request.user, wishlist_name='My Wishlist')
        wishlist_items = wishlist.items.all()
    except WishList.DoesNotExist:
        wishlist_items = []
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'products/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    """Add product to user's wishlist"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create user's default wishlist
    wishlist, created = WishList.objects.get_or_create(
        user=request.user,
        wishlist_name='My Wishlist'
    )
    
    # Check if item already in wishlist
    wishlist_item, created = WishListItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to your wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
    
    return redirect('product_detail', slug=product.slug)

@login_required
def remove_from_wishlist(request, item_id):
    """Remove item from wishlist"""
    wishlist_item = get_object_or_404(WishListItem, id=item_id, wishlist__user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.success(request, f'{product_name} removed from your wishlist!')
    return redirect('wishlist_view')
