# Generated by Django 5.0.3 on 2024-07-19 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_provider_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories_shop',
            field=models.ManyToManyField(related_name='products_shop', to='product.categoryshop'),
        ),
        migrations.AddField(
            model_name='provider',
            name='provider_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
