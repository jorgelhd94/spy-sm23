# Generated by Django 5.0.3 on 2024-06-27 21:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_remove_notificationnewinranking_higher_ranked_products_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='higherrankedproducts',
            name='notification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nr_products', to='notifications.notificationnewinranking'),
        ),
    ]
