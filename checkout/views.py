from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from home.models import Basket, BasketItem, Order, OrderItem
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    """Display checkout page with order summary"""
    try:
        basket = Basket.objects.get(user=request.user)
        basket_items = basket.items.all()

        if not basket_items:
            messages.error(request, 'Your basket is empty!')
            return redirect('basket_view')

        total = sum(item.product.price * item.quantity for item in basket_items)

        if request.method == 'POST':
            try:
                # Create order first
                order = Order.objects.create(
                    user=request.user,
                    total_price=total,
                    is_paid=False
                )

                # Create order items
                for item in basket_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                # Create Stripe payment intent
                intent = stripe.PaymentIntent.create(
                    amount=int(total * 100),  # Convert to pence
                    currency=settings.STRIPE_CURRENCY,
                    metadata={
                        'user_id': request.user.id,
                        'basket_id': basket.id,
                        'order_id': order.id,
                    }
                )

                # Update order with payment intent ID
                order.stripe_payment_intent_id = intent.id
                order.save()

                return JsonResponse({
                    'client_secret': intent.client_secret,
                    'order_id': order.id
                })

            except stripe.error.StripeError as e:
                messages.error(request, f'Payment error: {str(e)}')
                return redirect('checkout')

        context = {
            'basket_items': basket_items,
            'total': total,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'checkout/checkout.html', context)

    except Basket.DoesNotExist:
        messages.error(request, 'Your basket is empty!')
        return redirect('basket_view')

@login_required
@require_POST
def checkout_success(request):
    """Handle successful payment"""
    try:
        basket = Basket.objects.get(user=request.user)
        basket_items = basket.items.all()

        if not basket_items:
            messages.error(request, 'Your basket is empty!')
            return redirect('basket_view')

        # Calculate total
        total = sum(item.product.price * item.quantity for item in basket_items)

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            is_paid=True
        )

        # Create order items
        for basket_item in basket_items:
            OrderItem.objects.create(
                order=order,
                product=basket_item.product,
                quantity=basket_item.quantity,
                price=basket_item.product.price
            )

            # Update product stock
            product = basket_item.product
            product.stock -= basket_item.quantity
            product.save()

        # Clear basket
        basket_items.delete()

        messages.success(request, f'Order #{order.id} processed successfully!')
        return render(request, 'checkout/checkout_success.html', {'order': order})

    except Basket.DoesNotExist:
        messages.error(request, 'Your basket is empty!')
        return redirect('basket_view')

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']

        # Find the order by payment intent ID
        try:
            order = Order.objects.get(stripe_payment_intent_id=payment_intent['id'])
            order.is_paid = True
            order.save()

            # Clear the user's basket
            user_id = payment_intent['metadata'].get('user_id')
            if user_id:
                try:
                    basket = Basket.objects.get(user_id=user_id)
                    basket.items.all().delete()
                except Basket.DoesNotExist:
                    pass

        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)
