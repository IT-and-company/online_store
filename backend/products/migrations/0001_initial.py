from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название товара', max_length=250, verbose_name='Название товара')),
                ('text', models.TextField(blank=True, help_text='Напишите описание товара', verbose_name='Описание товара')),
                ('category', models.ManyToManyField(related_name='category', to='products.category', verbose_name='Категория товара')),
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
                'verbose_name_plural': 'размеры',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_number', models.CharField(blank=True, help_text='Введите артикул товара', max_length=250, verbose_name='Артикул товара')),
                ('model', models.CharField(help_text='Введите тип товара', max_length=250, verbose_name='Тип модели')),
                ('materials', models.CharField(help_text='Введите материлы товара', max_length=250, verbose_name='Материлы')),
                ('manufacturer', models.CharField(help_text='Введите Производителя', max_length=250, verbose_name='Производитель')),
                ('size', models.ManyToManyField(related_name='size_in_specific', to='products.size', verbose_name='Размер товара')),
            ],
            options={
                'verbose_name': 'Характеристика',
                'verbose_name_plural': 'Характеристики',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите тег', max_length=250, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(help_text='Укажите цвет тега', max_length=7, unique=True, verbose_name='Цвет тега')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Слаг тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
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
                ('image', models.ManyToManyField(to='products.image', verbose_name='Фотографии')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='products.product', verbose_name='Товары')),
                ('size', models.ManyToManyField(blank=True, related_name='size', to='products.size', verbose_name='Размер товара')),
                ('specification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='specification', to='products.specification')),
                ('tags', models.ManyToManyField(db_index=True, related_name='colour', to='products.tag', verbose_name='Цвет товара')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
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
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'default_related_name': 'favorite',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variationproduct', verbose_name='Товар')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
                'default_related_name': 'basket',
            },
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
