from django.shortcuts import render
import stripe
from django.conf import settings
from .models import Produto, Pedido
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
            'nome': 'Ésley Nathan',
            'endereco': 'Rua Dalia',
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

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        pedido = Pedido(produto_id= session['metadata']['id_produto'],
                        email=session['customer_details']['email'],
                        nome=session['metadata']['nome'],
                        endereco=session['metadata']['endereco'],
                        status=event['type'],
                        )
        pedido.save()

        print('Aprovada')

    return HttpResponse(status=200)