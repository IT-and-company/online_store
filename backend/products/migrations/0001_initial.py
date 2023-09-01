# Generated by Django 4.2.4 on 2023-09-01 10:50

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ColorTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(help_text='Введите тег', max_length=250, unique=True, verbose_name='Название цвета')),
                ('hex', models.CharField(help_text='Укажите цвет тега', max_length=7, unique=True, verbose_name='Код цвета')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Слаг цвета')),
            ],
            options={
                'verbose_name': 'Тег цвета',
                'verbose_name_plural': 'Теги цвета',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Загрузите фото товара', null=True, upload_to='product/%Y/%m/%d', verbose_name='Фото товара')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название товара', max_length=250, verbose_name='Название товара')),
                ('text', models.TextField(blank=True, help_text='Напишите описание товара', verbose_name='Описание товара')),
                ('category', models.ManyToManyField(to='products.category', verbose_name='Категория товара')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.PositiveSmallIntegerField(verbose_name='длина')),
                ('width', models.PositiveSmallIntegerField(verbose_name='ширина')),
                ('height', models.PositiveSmallIntegerField(verbose_name='высота')),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_number', models.CharField(blank=True, help_text='Введите артикул товара', max_length=250, verbose_name='Артикул товара')),
                ('feature_model', models.CharField(blank=True, help_text='Введите особенности товара', max_length=250, verbose_name='Особенности модели')),
                ('materials', models.CharField(help_text='Введите материалы товара', max_length=250, verbose_name='Материалы')),
                ('manufacturer', models.CharField(blank=True, help_text='Введите Производителя', max_length=250, verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Характеристика',
                'verbose_name_plural': 'Характеристики',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='VariationProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, default=0, verbose_name='Цена')),
                ('sale', models.IntegerField(blank=True, default=0, verbose_name='Скидка в процентах')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('color_tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.colortag', verbose_name='Цвет товара')),
                ('image', models.ManyToManyField(to='products.picture', verbose_name='Фотографии')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='products.product', verbose_name='Товары')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.size', verbose_name='Размер товара')),
                ('specification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='specification', to='products.specification')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.type', verbose_name='Тип товара')),
            ],
            options={
                'verbose_name': 'Модель',
                'verbose_name_plural': 'Модели',
                'ordering': ('name',),
            },
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
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variationproduct', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'default_related_name': 'favorite',
            },
        ),
    ]
