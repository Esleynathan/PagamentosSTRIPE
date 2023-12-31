# Generated by Django 4.2.3 on 2023-07-14 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0005_remove_pedido_payment_intent'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='payment_intent',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='valor_pago',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
