from django.contrib import admin
from .models import (
    Category, Product, ProductImage, Tag, ProductTag,
    Order, OrderItem, Basket, BasketItem, WishList, WishListItem
)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Product Image Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# Product Tag Inline
class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'original_price', 'stock', 'gender', 'size', 'created_at']
    list_filter = ['category', 'gender', 'size', 'created_at']
    search_fields = ['name', 'description', 'brand_name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductTagInline]

# Product Image Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_filter = ['product__category']

# Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

# Order Item Inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price']

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'is_paid', 'created_at']
    list_filter = ['is_paid', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline]

# Basket Item Inline
class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0

# Basket Admin
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    inlines = [BasketItemInline]

# Wishlist Item Inline
class WishListItemInline(admin.TabularInline):
    model = WishListItem
    extra = 0

# Wishlist Admin
@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['wishlist_name', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['wishlist_name', 'user__username']
    inlines = [WishListItemInline]
