# Technical Documentation - Nouveau Fit E-commerce Platform

## Overview

This document provides detailed technical information about the Nouveau Fit e-commerce platform, including architecture, implementation details, configuration, and deployment instructions.

## Architecture

### Django Apps Structure

#### 1. Home App (`home/`)
**Purpose**: Core functionality and main models
**Key Components**:
- **Models**: Product, Category, Order, OrderItem, Basket, BasketItem, WishList, Tag, ProductTag
- **Views**: Home page with featured products
- **Templates**: Home page layout with hero section, featured products, newsletter signup
- **Management Commands**: `create_sample_data` for populating test data

**Key Files**:
- `models.py`: Core database models
- `views.py`: Home page view logic
- `admin.py`: Django admin configuration
- `management/commands/create_sample_data.py`: Sample data creation

#### 2. Products App (`products/`)
**Purpose**: Product catalog and shopping cart functionality
**Key Components**:
- **Views**: Product listing, detail, search, basket management
- **Templates**: Product list, product detail, basket pages
- **URL Patterns**: Product-related routing

**Key Files**:
- `views.py`: Product catalog and basket logic
- `urls.py`: URL routing for products
- `templates/products/`: Product-related templates

#### 3. Checkout App (`checkout/`)
**Purpose**: Payment processing and order completion
**Key Components**:
- **Views**: Checkout process, Stripe integration, webhook handling
- **Templates**: Checkout form with Stripe payment
- **Payment Processing**: Real Stripe integration with GBP currency

**Key Files**:
- `views.py`: Checkout and payment logic
- `urls.py`: Checkout URL patterns
- `templates/checkout/`: Checkout templates

### Database Models

#### Core Models

**Product Model**
```python
class Product(models.Model):
    name = CharField(max_length=200)
    slug = SlugField(unique=True)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    original_price = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = PositiveIntegerField()
    category = ForeignKey(Category)
    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    size = CharField(max_length=10, choices=SIZE_CHOICES)
    material = CharField(max_length=100)
    brand_name = CharField(max_length=100)
    image = ImageField(upload_to='products/')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Order Model**
```python
class Order(models.Model):
    user = ForeignKey(User, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    is_paid = BooleanField(default=False)
    stripe_payment_intent_id = CharField(max_length=200, blank=True, null=True)
```

**Basket Model**
```python
class Basket(models.Model):
    user = ForeignKey(User, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### Model Relationships
- Product → Category (Many-to-One)
- Product → Tag (Many-to-Many through ProductTag)
- Order → User (Many-to-One)
- OrderItem → Order (Many-to-One)
- OrderItem → Product (Many-to-One)
- Basket → User (One-to-One)
- BasketItem → Basket (Many-to-One)
- BasketItem → Product (Many-to-One)

## Configuration Details

### Django Settings (`noveau_fit/settings.py`)

#### Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'home',
    'products',
    'checkout',
]
```

#### Middleware Configuration
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Static and Media Files
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### Authentication Settings (django-allauth)
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

#### Email Configuration
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
```

#### Stripe Configuration
```python
STRIPE_CURRENCY = 'gbp'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET')
```

### URL Configuration

#### Main URLs (`noveau_fit/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('checkout/', include('checkout.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### App-specific URLs
- **Home**: `/` (home page)
- **Products**: `/products/` (product listing), `/products/product/<slug>/` (product detail)
- **Checkout**: `/checkout/` (checkout page), `/checkout/success/` (success page)
- **Authentication**: `/accounts/login/`, `/accounts/signup/`, etc.

## Payment Integration

### Stripe Implementation

#### Frontend Integration
- Stripe.js v3 loaded in checkout template
- Card element for secure card input
- Real-time validation and error handling
- Payment confirmation flow

#### Backend Integration
```python
# Create payment intent
intent = stripe.PaymentIntent.create(
    amount=int(total * 100),  # Convert to pence
    currency=settings.STRIPE_CURRENCY,
    metadata={
        'user_id': request.user.id,
        'basket_id': basket.id,
        'order_id': order.id,
    }
)
```

#### Webhook Handling
- Endpoint: `/checkout/webhook/`
- Handles `payment_intent.succeeded` events
- Updates order status and clears basket
- Secure signature verification

### Payment Flow
1. User fills checkout form
2. Frontend creates payment intent via AJAX
3. Stripe processes payment
4. Webhook confirms payment success
5. Order marked as paid, basket cleared
6. User redirected to success page

## Email Configuration Setup

### Gmail SMTP Setup

1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Enable 2-factor authentication

2. **Generate App Password**
   - Go to Google Account > Security
   - Select "App passwords"
   - Generate password for "Mail"

3. **Environment Variables**
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-character-app-password
   ```

### Email Verification Flow
1. User registers with email
2. Verification email sent automatically
3. User clicks verification link
4. Account activated
5. User can login

### Custom Email Templates
Located in `templates/account/email/`:
- `email_confirmation_message.txt`
- `email_confirmation_subject.txt`
- `password_reset_key_message.txt`

## Stripe Payment Setup Guide

### Development Setup

1. **Create Stripe Account**
   - Visit https://stripe.com
   - Create account and verify email

2. **Get Test API Keys**
   - Dashboard > Developers > API keys
   - Copy "Publishable key" (pk_test_...)
   - Copy "Secret key" (sk_test_...)

3. **Setup Webhook Endpoint**
   - Dashboard > Developers > Webhooks
   - Add endpoint: `http://localhost:8000/checkout/webhook/`
   - Select event: `payment_intent.succeeded`
   - Copy webhook secret (whsec_...)

4. **Environment Configuration**
   ```env
   STRIPE_PUBLIC_KEY=pk_test_your_publishable_key
   STRIPE_SECRET_KEY=sk_test_your_secret_key
   STRIPE_WH_SECRET=whsec_your_webhook_secret
   ```

### Production Setup

1. **Activate Stripe Account**
   - Complete business verification
   - Provide required documentation

2. **Get Live API Keys**
   - Switch to live mode in dashboard
   - Copy live API keys (pk_live_... and sk_live_...)

3. **Update Webhook Endpoint**
   - Change endpoint to production URL
   - Update webhook secret

4. **Production Environment Variables**
   ```env
   STRIPE_PUBLIC_KEY=pk_live_your_live_publishable_key
   STRIPE_SECRET_KEY=sk_live_your_live_secret_key
   STRIPE_WH_SECRET=whsec_your_live_webhook_secret
   ```

### Testing Payments

Use Stripe test card numbers:
- **Success**: 4242 4242 4242 4242
- **Declined**: 4000 0000 0000 0002
- **Requires Authentication**: 4000 0025 0000 3155

## Security Considerations

### CSRF Protection
- CSRF tokens in all forms
- CSRF exempt only for webhook endpoint

### Authentication
- django-allauth for secure authentication
- Email verification required
- Password strength validation

### Payment Security
- No card data stored locally
- Stripe handles all sensitive data
- Webhook signature verification

### Environment Variables
- Sensitive data in environment variables
- Never commit secrets to version control
- Use different keys for development/production

## Performance Optimization

### Database
- Proper indexing on frequently queried fields
- Select_related and prefetch_related for queries
- Database connection pooling for production

### Static Files
- Collectstatic for production
- CDN integration ready
- Compressed CSS/JS for production

### Caching
- Template fragment caching ready
- Database query caching
- Redis integration ready

## Deployment Checklist

### Pre-deployment
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production database
- [ ] Configure static file serving
- [ ] Set up email backend
- [ ] Configure Stripe live keys
- [ ] Set up SSL/HTTPS
- [ ] Configure domain settings

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
STRIPE_PUBLIC_KEY=pk_live_your_live_key
STRIPE_SECRET_KEY=sk_live_your_live_key
STRIPE_WH_SECRET=whsec_your_live_webhook_secret
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Post-deployment
- [ ] Run migrations
- [ ] Collect static files
- [ ] Create superuser
- [ ] Test payment flow
- [ ] Test email sending
- [ ] Monitor error logs
- [ ] Set up backup strategy

## Troubleshooting

### Common Issues

**Stripe Webhook Failures**
- Check webhook endpoint URL
- Verify webhook secret
- Check server logs for errors

**Email Not Sending**
- Verify SMTP settings
- Check app password for Gmail
- Test email configuration

**Static Files Not Loading**
- Run `collectstatic` command
- Check STATIC_ROOT setting
- Verify web server configuration

**Database Errors**
- Run migrations: `python manage.py migrate`
- Check database permissions
- Verify database connection settings

### Debug Mode
Enable debug mode for development:
```python
DEBUG = True
```

Never enable debug mode in production.

## Monitoring and Logging

### Error Tracking
- Configure Sentry for production error tracking
- Set up log aggregation
- Monitor payment failures

### Performance Monitoring
- Database query monitoring
- Response time tracking
- Resource usage monitoring

### Business Metrics
- Order conversion rates
- Payment success rates
- User registration rates
- Product performance metrics
