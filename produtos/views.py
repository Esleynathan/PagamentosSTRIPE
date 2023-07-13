from django.shortcuts import render
import stripe
from django.conf import settings
from .models import Produto, Pedido
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment(request, id):
    produto = Produto.objects.get (id = id)
    print(request.body)
    
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=int(produto.preco),
        currency='BRL',
        )
    return JsonResponse({
        'clientSecret': intent['client_secret']
         })


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