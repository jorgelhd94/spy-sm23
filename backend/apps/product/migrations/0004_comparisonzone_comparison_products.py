# Generated by Django 5.0.3 on 2024-04-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_comparisonzone_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparisonzone',
            name='comparison_products',
            field=models.ManyToManyField(related_name='comparison_zones', to='product.product'),
        ),
    ]
