# Generated by Django 4.2.2 on 2023-07-10 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='app.OrderItem', to='app.product'),
        ),
    ]
