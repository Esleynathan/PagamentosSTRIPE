from django.shortcuts import render
import stripe
from django.conf import settings
from .models import Produto
from django.http import JsonResponse, HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, id):
    produto = Produto.objects.get(id = id)
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'BRL',
                    'unit_amount': int(produto.preco),
                    'product_data': {
                    'name': produto.nome
                    }

                },
                'quantity': 1,
            },
        ],
        payment_method_types=[
            'card',
            'boleto',
        ],
        metadata={
            'id_produto': produto.id,
        },
        mode='payment',
        success_url=YOUR_DOMAIN + '/sucesso',
        cancel_url=YOUR_DOMAIN + '/erro',
    )
    return JsonResponse({'id': checkout_session.id})


def home(request):
    produto = Produto.objects.get(id = 1)

    return render(request, 'home.html',{'produto': produto, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})


def sucesso(request):
    return HttpResponse('Sucesso!')

def erro(request):
    return HttpResponse('Erro!')