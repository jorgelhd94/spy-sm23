# Generated by Django 5.0.3 on 2024-06-10 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics_spy', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductUpdate',
            new_name='ProductsUpdateLogs',
        ),
    ]
