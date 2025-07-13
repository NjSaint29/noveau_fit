from django.urls import path
from . import views, profile_views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('basket/', views.basket_view, name='basket_view'),
    path('update-basket/<int:item_id>/', views.update_basket_item, name='update_basket_item'),
    path('remove-from-basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),

    # Profile and wishlist URLs
    path('profile/', profile_views.profile_view, name='profile_view'),
    path('wishlist/', profile_views.wishlist_view, name='wishlist_view'),
    path('add-to-wishlist/<int:product_id>/', profile_views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:item_id>/', profile_views.remove_from_wishlist, name='remove_from_wishlist'),
]
