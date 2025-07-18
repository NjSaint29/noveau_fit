# Nouveau Fit - Django E-commerce Platform

A modern, full-featured e-commerce platform built with Django, featuring user authentication, product management, shopping cart functionality, and Stripe payment integration.

## Features

- **User Authentication**: Complete user registration, login, and profile management using django-allauth
- **Product Management**: Categories, products with images, stock management, and filtering
- **Shopping Cart**: Add/remove items, quantity management, persistent cart
- **Secure Payments**: Stripe integration with real payment processing (GBP currency)
- **Order Management**: Order history, order tracking, and status updates
- **Responsive Design**: Mobile-friendly Bootstrap-based UI
- **Admin Interface**: Django admin for managing products, orders, and users
- **Email Integration**: Email verification and order confirmations
- **Wishlist**: Save products for later
- **Search & Filtering**: Product search and category filtering

## Technology Stack

- **Backend**: Django 5.1.5, Python 3.13
- **Database**: SQLite (development), PostgreSQL ready
- **Frontend**: Bootstrap 4, HTML5, CSS3, JavaScript
- **Payment Processing**: Stripe API
- **Authentication**: django-allauth
- **Image Handling**: Pillow
- **Deployment Ready**: Configured for production deployment

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/guerric-k/noveau_fit.git
   cd noveau_fit
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_WH_SECRET=whsec_your_webhook_secret
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py create_sample_data
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
noveau_fit/
├── noveau_fit/           # Main project settings
│   ├── settings.py       # Django settings and configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── home/                # Home app (main functionality)
│   ├── models.py        # Core models (Product, Order, Basket, etc.)
│   ├── views.py         # Home page views
│   ├── templates/       # Home page templates
│   └── management/      # Custom management commands
├── products/            # Product management app
│   ├── views.py         # Product listing, detail, search views
│   ├── templates/       # Product-related templates
│   └── urls.py          # Product URL patterns
├── checkout/            # Checkout and payment app
│   ├── views.py         # Checkout, payment, Stripe integration
│   ├── templates/       # Checkout templates
│   └── urls.py          # Checkout URL patterns
├── templates/           # Global templates
│   ├── base.html        # Base template
│   ├── allauth/         # Authentication templates
│   └── includes/        # Reusable template components
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
└── requirements.txt     # Python dependencies
```

## Configuration Guide

### Stripe Payment Setup

1. **Create Stripe Account**
   - Go to https://stripe.com and create an account
   - Navigate to Developers > API keys

2. **Get API Keys**
   - Copy your Publishable key (pk_test_...)
   - Copy your Secret key (sk_test_...)

3. **Setup Webhooks**
   - Go to Developers > Webhooks
   - Add endpoint: `https://yourdomain.com/checkout/webhook/`
   - Select events: `payment_intent.succeeded`
   - Copy the webhook secret (whsec_...)

4. **Update Settings**
   Add to your `.env` file:
   ```env
   STRIPE_PUBLIC_KEY=pk_test_your_key_here
   STRIPE_SECRET_KEY=sk_test_your_key_here
   STRIPE_WH_SECRET=whsec_your_webhook_secret
   ```

### Email Configuration

For Gmail SMTP:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note**: Use App Passwords for Gmail, not your regular password.

## Usage Guide

### Admin Interface

1. Create superuser: `python manage.py createsuperuser`
2. Access admin at: http://127.0.0.1:8000/admin/
3. Manage:
   - Products and categories
   - Orders and order items
   - Users and authentication
   - Site configuration

### Adding Products

1. Log into admin interface
2. Go to "Products" section
3. Add categories first
4. Add products with:
   - Name, description, price
   - Category assignment
   - Stock quantity
   - Product images
   - Tags for filtering

### Managing Orders

- View all orders in admin
- Track order status
- View order items and customer details
- Process refunds through Stripe dashboard

## Development

### Custom Management Commands

- `python manage.py create_sample_data` - Creates sample products and categories

### Database Models

**Core Models:**
- `Product`: Product information, pricing, stock
- `Category`: Product categorization
- `Order`: Customer orders
- `OrderItem`: Individual items in orders
- `Basket`: Shopping cart functionality
- `BasketItem`: Items in shopping cart
- `WishList`: User wishlists

### API Endpoints

- `/` - Home page with featured products
- `/products/` - Product listing with filtering
- `/products/product/<slug>/` - Product detail page
- `/products/basket/` - Shopping cart
- `/checkout/` - Checkout process
- `/checkout/webhook/` - Stripe webhook handler
- `/accounts/` - Authentication (login, register, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
