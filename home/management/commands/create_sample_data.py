from django.core.management.base import BaseCommand
from home.models import Category, Product, Tag, ProductTag

class Command(BaseCommand):
    help = 'Create sample data for the e-commerce site'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'T-Shirts', 'slug': 't-shirts'},
            {'name': 'Jeans', 'slug': 'jeans'},
            {'name': 'Dresses', 'slug': 'dresses'},
            {'name': 'Shoes', 'slug': 'shoes'},
            {'name': 'Accessories', 'slug': 'accessories'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create tags
        tags_data = ['casual', 'formal', 'summer', 'winter', 'trendy', 'classic', 'sport']
        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags[tag_name] = tag
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
        
        # Create products
        products_data = [
            {
                'name': 'Classic White T-Shirt',
                'slug': 'classic-white-t-shirt',
                'description': 'A comfortable and versatile white t-shirt perfect for everyday wear.',
                'price': 19.99,
                'original_price': 24.99,
                'stock': 50,
                'category': 't-shirts',
                'gender': 'U',
                'size': 'M',
                'material': 'Cotton',
                'brand_name': 'Nouveau Basics',
                'tags': ['casual', 'classic']
            },
            {
                'name': 'Slim Fit Blue Jeans',
                'slug': 'slim-fit-blue-jeans',
                'description': 'Modern slim-fit jeans in classic blue denim.',
                'price': 79.99,
                'stock': 30,
                'category': 'jeans',
                'gender': 'M',
                'size': 'L',
                'material': 'Denim',
                'brand_name': 'Nouveau Denim',
                'tags': ['casual', 'classic']
            },
            {
                'name': 'Summer Floral Dress',
                'slug': 'summer-floral-dress',
                'description': 'Beautiful floral dress perfect for summer occasions.',
                'price': 89.99,
                'original_price': 109.99,
                'stock': 25,
                'category': 'dresses',
                'gender': 'W',
                'size': 'M',
                'material': 'Polyester',
                'brand_name': 'Nouveau Elegance',
                'tags': ['summer', 'formal', 'trendy']
            },
            {
                'name': 'Running Sneakers',
                'slug': 'running-sneakers',
                'description': 'Comfortable running sneakers with excellent support.',
                'price': 129.99,
                'stock': 40,
                'category': 'shoes',
                'gender': 'U',
                'size': 'L',
                'material': 'Synthetic',
                'brand_name': 'Nouveau Sport',
                'tags': ['sport', 'casual']
            },
            {
                'name': 'Leather Handbag',
                'slug': 'leather-handbag',
                'description': 'Elegant leather handbag for everyday use.',
                'price': 159.99,
                'original_price': 199.99,
                'stock': 15,
                'category': 'accessories',
                'gender': 'W',
                'size': 'M',
                'material': 'Leather',
                'brand_name': 'Nouveau Luxury',
                'tags': ['formal', 'classic']
            },
            {
                'name': 'Casual Black T-Shirt',
                'slug': 'casual-black-t-shirt',
                'description': 'Comfortable black t-shirt for casual wear.',
                'price': 22.99,
                'stock': 60,
                'category': 't-shirts',
                'gender': 'M',
                'size': 'L',
                'material': 'Cotton',
                'brand_name': 'Nouveau Basics',
                'tags': ['casual']
            },
            {
                'name': 'High-Waist Skinny Jeans',
                'slug': 'high-waist-skinny-jeans',
                'description': 'Trendy high-waist skinny jeans for women.',
                'price': 69.99,
                'stock': 35,
                'category': 'jeans',
                'gender': 'W',
                'size': 'S',
                'material': 'Denim',
                'brand_name': 'Nouveau Denim',
                'tags': ['trendy', 'casual']
            },
            {
                'name': 'Winter Wool Coat',
                'slug': 'winter-wool-coat',
                'description': 'Warm and stylish wool coat for winter.',
                'price': 249.99,
                'stock': 20,
                'category': 'accessories',
                'gender': 'W',
                'size': 'M',
                'material': 'Wool',
                'brand_name': 'Nouveau Winter',
                'tags': ['winter', 'formal']
            }
        ]
        
        for product_data in products_data:
            category = categories[product_data['category']]
            product_tags = product_data.pop('tags')
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
                
                # Add tags to product
                for tag_name in product_tags:
                    tag = tags[tag_name]
                    ProductTag.objects.get_or_create(product=product, tag=tag)
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
