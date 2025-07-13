# Deployment Guide - Nouveau Fit E-commerce Platform

## Overview

This guide covers deployment options and step-by-step instructions for deploying the Nouveau Fit e-commerce platform to various hosting providers.

## Pre-Deployment Checklist

### Code Preparation
- [ ] All features tested locally
- [ ] Database migrations created and tested
- [ ] Static files collected and tested
- [ ] Environment variables documented
- [ ] Requirements.txt updated
- [ ] Debug mode disabled
- [ ] Security settings configured

### Third-Party Services
- [ ] Stripe account activated (for live payments)
- [ ] Email service configured
- [ ] Domain name registered (if needed)
- [ ] SSL certificate ready

## Environment Configuration

### Production Environment Variables

Create a `.env` file or set environment variables:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-production-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (varies by provider)
DATABASE_URL=postgres://user:password@host:port/database

# Stripe (Live Keys)
STRIPE_PUBLIC_KEY=pk_live_your_live_publishable_key
STRIPE_SECRET_KEY=sk_live_your_live_secret_key
STRIPE_WH_SECRET=whsec_your_live_webhook_secret

# Email Configuration
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password

# Static Files (if using cloud storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## Deployment Options

### Option 1: Heroku Deployment

#### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

#### Step 1: Prepare for Heroku
1. **Install dependencies**
   ```bash
   pip install gunicorn dj-database-url whitenoise
   ```

2. **Create Procfile**
   ```
   web: gunicorn noveau_fit.wsgi:application
   release: python manage.py migrate
   ```

3. **Update settings for Heroku**
   Add to `settings.py`:
   ```python
   import dj_database_url
   
   # Database
   if 'DATABASE_URL' in os.environ:
       DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'])
   
   # Static files
   MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

#### Step 2: Deploy to Heroku
1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set STRIPE_PUBLIC_KEY=pk_live_your_key
   heroku config:set STRIPE_SECRET_KEY=sk_live_your_key
   heroku config:set STRIPE_WH_SECRET=whsec_your_secret
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Create superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

#### Step 3: Configure Stripe Webhook
- Update webhook endpoint to: `https://your-app-name.herokuapp.com/checkout/webhook/`

### Option 2: DigitalOcean App Platform

#### Step 1: Prepare Repository
1. **Create app.yaml**
   ```yaml
   name: nouveau-fit
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/noveau_fit
       branch: main
     run_command: gunicorn noveau_fit.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: DEBUG
       value: "False"
     - key: SECRET_KEY
       value: your-secret-key
       type: SECRET
     - key: STRIPE_PUBLIC_KEY
       value: pk_live_your_key
       type: SECRET
     - key: STRIPE_SECRET_KEY
       value: sk_live_your_key
       type: SECRET
   databases:
   - name: db
     engine: PG
     version: "13"
   ```

#### Step 2: Deploy
1. Connect GitHub repository
2. Configure environment variables
3. Add PostgreSQL database
4. Deploy application

### Option 3: AWS Elastic Beanstalk

#### Step 1: Prepare for AWS
1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Create .ebextensions/django.config**
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: noveau_fit.wsgi:application
     aws:elasticbeanstalk:application:environment:
       DJANGO_SETTINGS_MODULE: noveau_fit.settings
   ```

#### Step 2: Deploy
1. **Initialize EB**
   ```bash
   eb init
   ```

2. **Create environment**
   ```bash
   eb create production
   ```

3. **Set environment variables**
   ```bash
   eb setenv DEBUG=False SECRET_KEY=your-key
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

### Option 4: Railway

#### Step 1: Connect Repository
1. Go to Railway.app
2. Connect GitHub repository
3. Select noveau_fit repository

#### Step 2: Configure
1. **Add PostgreSQL service**
2. **Set environment variables**:
   - DEBUG=False
   - SECRET_KEY=your-secret-key
   - STRIPE_PUBLIC_KEY=pk_live_your_key
   - STRIPE_SECRET_KEY=sk_live_your_key
   - STRIPE_WH_SECRET=whsec_your_secret

#### Step 3: Deploy
Railway automatically deploys on git push.

## Database Migration

### For all platforms:
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py create_sample_data
```

## Static Files Configuration

### Option 1: WhiteNoise (Simple)
Add to `settings.py`:
```python
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Option 2: AWS S3 (Recommended for production)
1. **Install django-storages**
   ```bash
   pip install django-storages boto3
   ```

2. **Configure settings**
   ```python
   # AWS S3 Settings
   AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
   AWS_S3_REGION_NAME = 'us-east-1'
   AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
   
   # Static files
   STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   
   STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
   MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
   ```

## Domain and SSL Configuration

### Custom Domain Setup
1. **Point domain to hosting provider**
2. **Configure ALLOWED_HOSTS**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

### SSL Certificate
Most hosting providers offer free SSL certificates:
- **Heroku**: Automatic SSL for custom domains
- **DigitalOcean**: Let's Encrypt integration
- **Railway**: Automatic SSL
- **AWS**: Use AWS Certificate Manager

## Post-Deployment Tasks

### 1. Test Core Functionality
- [ ] Home page loads correctly
- [ ] User registration/login works
- [ ] Product pages display properly
- [ ] Shopping cart functionality
- [ ] Checkout process completes
- [ ] Payment processing works
- [ ] Email sending works
- [ ] Admin interface accessible

### 2. Configure Monitoring
- **Error Tracking**: Set up Sentry
- **Uptime Monitoring**: Use UptimeRobot or similar
- **Performance Monitoring**: Configure APM tools

### 3. Backup Strategy
- **Database Backups**: Automated daily backups
- **Media Files**: Regular backup of uploaded files
- **Code Backups**: Git repository with multiple remotes

### 4. Security Hardening
- **HTTPS Only**: Force HTTPS redirects
- **Security Headers**: Configure security middleware
- **Rate Limiting**: Implement rate limiting
- **Regular Updates**: Keep dependencies updated

## Troubleshooting Common Issues

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT setting
# Verify web server configuration
```

### Database Connection Errors
```python
# Check DATABASE_URL format
# Verify database credentials
# Ensure database server is accessible
```

### Stripe Webhook Issues
- Update webhook endpoint URL to production domain
- Verify webhook secret matches
- Check webhook endpoint is accessible

### Email Not Sending
- Verify SMTP settings
- Check email service credentials
- Test email configuration

## Performance Optimization

### Database Optimization
- **Connection Pooling**: Use pgbouncer for PostgreSQL
- **Query Optimization**: Use select_related and prefetch_related
- **Indexing**: Add database indexes for frequently queried fields

### Caching
```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### CDN Integration
- Use CloudFlare or AWS CloudFront
- Configure static file caching
- Optimize image delivery

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Multiple application instances
- Shared session storage

### Database Scaling
- Read replicas for read-heavy workloads
- Database connection pooling
- Query optimization

### File Storage
- Cloud storage for media files
- CDN for static file delivery
- Image optimization and compression

## Maintenance

### Regular Tasks
- **Security Updates**: Monthly dependency updates
- **Database Maintenance**: Regular cleanup and optimization
- **Backup Verification**: Test backup restoration
- **Performance Monitoring**: Review metrics and optimize

### Monitoring Checklist
- [ ] Application uptime
- [ ] Response times
- [ ] Error rates
- [ ] Database performance
- [ ] Payment success rates
- [ ] Email delivery rates

## Support and Documentation

### Logging
Configure comprehensive logging:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Checks
Implement health check endpoints for monitoring:
```python
# Add to urls.py
path('health/', health_check_view, name='health_check'),
```

This deployment guide provides comprehensive instructions for deploying the Nouveau Fit e-commerce platform to various hosting providers with proper configuration and monitoring.
