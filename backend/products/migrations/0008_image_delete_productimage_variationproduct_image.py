# Generated by Django 4.2.3 on 2023-07-28 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productimage_remove_variationproduct_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Загрузите фото товара', null=True, upload_to='product/%Y/%m/%d', verbose_name='Фото товара')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
        migrations.AddField(
            model_name='variationproduct',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictures', to='products.image', verbose_name='Фотографии'),
        ),
    ]
