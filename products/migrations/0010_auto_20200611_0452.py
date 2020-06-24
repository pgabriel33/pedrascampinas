# Generated by Django 3.0.7 on 2020-06-11 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200611_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='status_da_compra',
            field=models.PositiveIntegerField(choices=[[55, 'Em Analise'], [56, 'Aguardando Pagamento'], [57, 'Pagamento Aprovado'], [58, 'Preparando Entrega'], [59, 'Transportadora'], [60, 'Pedidos Entregues']], default=55, verbose_name='Status da Compra'),
        ),
    ]