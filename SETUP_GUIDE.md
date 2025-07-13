# Setup Guide - Nouveau Fit E-commerce Platform

## Complete Development Setup

This guide provides step-by-step instructions for setting up the Nouveau Fit e-commerce platform for development.

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher (3.13 recommended)
- **pip**: Latest version
- **Git**: For version control
- **Code Editor**: VS Code, PyCharm, or similar

### Third-Party Accounts Needed
- **Stripe Account**: For payment processing
- **Gmail Account**: For email functionality (or other SMTP service)

## Step 1: Project Setup

### 1.1 Clone Repository
```bash
git clone https://github.com/guerric-k/noveau_fit.git
cd noveau_fit
```

### 1.2 Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Environment Configuration

### 2.1 Create Environment File
Create a `.env` file in the project root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe Settings (Test Keys)
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WH_SECRET=whsec_your_webhook_secret_here

# Email Settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here

# Database (optional - defaults to SQLite)
# DATABASE_URL=sqlite:///db.sqlite3
```

### 2.2 Generate Secret Key
```python
# Run this in Python shell to generate a secret key
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 3: Stripe Configuration

### 3.1 Create Stripe Account
1. Go to https://stripe.com
2. Click "Start now" and create an account
3. Complete email verification

### 3.2 Get Test API Keys
1. Log into Stripe Dashboard
2. Navigate to **Developers** > **API keys**
3. Copy the **Publishable key** (starts with `pk_test_`)
4. Copy the **Secret key** (starts with `sk_test_`)
5. Add these to your `.env` file

### 3.3 Setup Webhook for Local Development
1. Install Stripe CLI:
   ```bash
   # Download from https://stripe.com/docs/stripe-cli
   # Or use package manager:
   # Windows (with Chocolatey): choco install stripe-cli
   # macOS (with Homebrew): brew install stripe/stripe-cli/stripe
   ```

2. Login to Stripe CLI:
   ```bash
   stripe login
   ```

3. Forward events to local server:
   ```bash
   stripe listen --forward-to localhost:8000/checkout/webhook/
   ```

4. Copy the webhook secret (starts with `whsec_`) to your `.env` file

### 3.4 Alternative: Manual Webhook Setup
1. In Stripe Dashboard, go to **Developers** > **Webhooks**
2. Click **Add endpoint**
3. Enter endpoint URL: `http://localhost:8000/checkout/webhook/`
4. Select events: `payment_intent.succeeded`
5. Copy the webhook secret to your `.env` file

## Step 4: Email Configuration

### 4.1 Gmail Setup (Recommended for Development)

#### Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to **Security**
3. Enable **2-Step Verification**

#### Generate App Password
1. In Google Account settings, go to **Security**
2. Under "2-Step Verification", click **App passwords**
3. Select **Mail** as the app
4. Copy the generated 16-character password
5. Add to your `.env` file as `EMAIL_HOST_PASSWORD`

### 4.2 Alternative Email Services

#### SendGrid
```env
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your-sendgrid-api-key
```

#### Mailgun
```env
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=your-mailgun-username
EMAIL_HOST_PASSWORD=your-mailgun-password
```

## Step 5: Database Setup

### 5.1 Run Migrations
```bash
python manage.py migrate
```

### 5.2 Create Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

### 5.3 Load Sample Data
```bash
python manage.py create_sample_data
```
This creates sample products, categories, and tags for testing.

## Step 6: Static Files Setup

### 6.1 Collect Static Files (if needed)
```bash
python manage.py collectstatic
```

### 6.2 Create Media Directory
```bash
mkdir media
mkdir media/products
```

## Step 7: Run Development Server

### 7.1 Start Django Server
```bash
python manage.py runserver
```

### 7.2 Access Application
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Step 8: Testing the Setup

### 8.1 Test Basic Functionality
1. **Home Page**: Visit http://127.0.0.1:8000/
2. **Product Listing**: Click "Shop Collection" or visit `/products/`
3. **User Registration**: Click "My Account" > "Register"
4. **Admin Panel**: Visit `/admin/` and login with superuser credentials

### 8.2 Test Email Functionality
1. Register a new user account
2. Check your email for verification message
3. Click verification link to activate account

### 8.3 Test Payment Flow
1. Add products to basket
2. Go to checkout
3. Use Stripe test card: `4242 4242 4242 4242`
4. Complete payment process

## Step 9: Development Workflow

### 9.1 Making Changes
1. **Models**: After changing models, run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Static Files**: After changing CSS/JS:
   ```bash
   python manage.py collectstatic
   ```

3. **Templates**: Changes are reflected immediately

### 9.2 Adding Products via Admin
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Navigate to **Products** > **Categories** and add categories
4. Navigate to **Products** > **Products** and add products
5. Upload product images in the admin interface

## Step 10: Troubleshooting

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError"
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Issue: "CSRF verification failed"
**Solution**: Ensure CSRF tokens are included in forms and CSRF middleware is enabled.

#### Issue: "Stripe webhook signature verification failed"
**Solution**: 
- Check webhook secret in `.env` file
- Ensure webhook endpoint is accessible
- Verify Stripe CLI is forwarding events correctly

#### Issue: "Email not sending"
**Solution**:
- Verify Gmail app password is correct
- Check email settings in `settings.py`
- Ensure 2-factor authentication is enabled on Gmail

#### Issue: "Static files not loading"
**Solution**:
```bash
python manage.py collectstatic
```
Check `STATIC_URL` and `STATICFILES_DIRS` in settings.

#### Issue: "Database locked" (SQLite)
**Solution**: Ensure no other processes are accessing the database file.

### Debug Mode
For debugging, ensure these settings in your `.env`:
```env
DEBUG=True
```

### Logging
Check Django logs for detailed error information:
```bash
# View recent logs
tail -f django.log
```

## Step 11: Optional Enhancements

### 11.1 Install Development Tools
```bash
pip install django-debug-toolbar django-extensions
```

Add to `INSTALLED_APPS` in settings.py:
```python
INSTALLED_APPS = [
    # ... existing apps
    'debug_toolbar',
    'django_extensions',
]
```

### 11.2 Database GUI (Optional)
- **SQLite**: DB Browser for SQLite
- **PostgreSQL**: pgAdmin
- **General**: DBeaver

### 11.3 API Testing (Optional)
- **Postman**: For testing API endpoints
- **HTTPie**: Command-line HTTP client

## Step 12: Production Preparation

### 12.1 Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
STRIPE_PUBLIC_KEY=pk_live_your_live_key
STRIPE_SECRET_KEY=sk_live_your_live_key
```

### 12.2 Security Checklist
- [ ] Change SECRET_KEY for production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS in production
- [ ] Use live Stripe keys
- [ ] Set up proper email backend
- [ ] Configure database backups

## Support

### Getting Help
1. **Documentation**: Check README.md and TECHNICAL_DOCUMENTATION.md
2. **Django Documentation**: https://docs.djangoproject.com/
3. **Stripe Documentation**: https://stripe.com/docs
4. **GitHub Issues**: Create an issue for bugs or questions

### Useful Commands
```bash
# Check Django version
python -m django --version

# Run tests
python manage.py test

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Django shell
python manage.py shell

# Load sample data
python manage.py create_sample_data
```

This setup guide should get you up and running with the Nouveau Fit e-commerce platform. Follow each step carefully and refer to the troubleshooting section if you encounter any issues.
