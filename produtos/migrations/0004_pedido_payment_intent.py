# Generated by Django 4.2.3 on 2023-07-14 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_rename_produto_pedido_produto_remove_pedido_endereco_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='payment_intent',
            field=models.CharField(default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
    ]
