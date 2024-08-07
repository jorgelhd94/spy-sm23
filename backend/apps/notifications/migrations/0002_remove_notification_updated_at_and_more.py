# Generated by Django 5.0.3 on 2024-06-27 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        ('product', '0005_product_previous_price_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='updated_at',
        ),
        migrations.CreateModel(
            name='NotificationNewInRanking',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notifications.notification')),
                ('higher_ranked_products', models.ManyToManyField(related_name='nr_ranked_notifications', to='product.product')),
                ('provider_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nr_provider_notifications', to='product.product')),
            ],
            options={
                'db_table': 'notification_new_in_ranking',
            },
            bases=('notifications.notification',),
        ),
    ]
