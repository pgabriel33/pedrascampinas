# Generated by Django 2.2.6 on 2020-05-25 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.PositiveIntegerField(choices=[[0, 'Quartzo'], [1, 'Seixo'], [3, 'Laje'], [4, 'Serrada']], verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='cor',
            field=models.PositiveIntegerField(choices=[[0, 'Rosa'], [1, 'Branco'], [2, 'Verde']], verbose_name='Cor'),
        ),
    ]
