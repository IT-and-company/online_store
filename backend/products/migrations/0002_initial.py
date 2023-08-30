# Generated by Django 4.2.4 on 2023-08-30 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='specification',
            name='size',
            field=models.ManyToManyField(related_name='size_in_specific', to='products.size', verbose_name='Размер товара'),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.type', verbose_name='Тип товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='category', to='products.category', verbose_name='Категория товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='model',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='type', chained_model_field='type', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='products.productmodel', verbose_name='Модель товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.type', verbose_name='Тип товара'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variationproduct', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.usercart', verbose_name='Корзина'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartproduct', to='products.variationproduct', verbose_name='Продукт'),
        ),
        migrations.AddField(
            model_name='basket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variationproduct', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('name', 'type'), name='unique_type'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_favorite'),
        ),
        migrations.AddConstraint(
            model_name='basket',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_basket'),
        ),
    ]
