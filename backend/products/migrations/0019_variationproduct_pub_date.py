# Generated by Django 4.2.4 on 2023-08-11 07:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_remove_variationproduct_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='variationproduct',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
    ]