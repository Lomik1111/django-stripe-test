import stripe
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Item

# Настраиваем Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def item_detail(request, id):
    """Страница товара с кнопкой покупки"""
    item = get_object_or_404(Item, id=id)
    context = {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'shop/item_detail.html', context)

@csrf_exempt
def buy_item(request, id):
    """API для создания Stripe Session"""
    item = get_object_or_404(Item, id=id)
    
    try:
        # Создаем сессию оплаты в Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': item.get_price_in_cents(),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri(f'/item/{item.id}/'),
        )
        
        # Возвращаем ID сессии
        return JsonResponse({'id': checkout_session.id})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def success_view(request):
    """Страница успешной оплаты"""
    return render(request, 'shop/success.html')