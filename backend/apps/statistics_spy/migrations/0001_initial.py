# Generated by Django 5.0.3 on 2024-06-10 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('processing', 'Procesando'), ('success', 'Éxito'), ('error', 'Error')], max_length=10)),
                ('note', models.TextField(blank=True, null=True)),
                ('updated_products_count', models.IntegerField(default=0)),
                ('deleted_products_count', models.IntegerField(default=0)),
                ('new_products_count', models.IntegerField(default=0)),
            ],
        ),
    ]
