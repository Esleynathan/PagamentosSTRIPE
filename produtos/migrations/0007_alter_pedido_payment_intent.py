# Generated by Django 4.2.3 on 2023-07-14 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0006_pedido_payment_intent_pedido_valor_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='payment_intent',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
