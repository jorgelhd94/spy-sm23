# Generated by Django 5.0.3 on 2024-04-01 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comparisonzone',
            name='comparison_products',
        ),
        migrations.AlterField(
            model_name='comparisonzone',
            name='main_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_comparison_zones', to='product.product'),
        ),
    ]
