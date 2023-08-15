# Generated by Django 4.2.4 on 2023-08-15 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_variationproduct_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Введите название товара', max_length=250, verbose_name='Название товара'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='article_number',
            field=models.CharField(blank=True, help_text='Введите артикул товара', max_length=250, verbose_name='Артикул товара'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='manufacturer',
            field=models.CharField(help_text='Введите Производителя', max_length=250, verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='materials',
            field=models.CharField(help_text='Введите материлы товара', max_length=250, verbose_name='Материлы'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='model',
            field=models.CharField(help_text='Введите тип товара', max_length=250, verbose_name='Тип модели'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Введите тег', max_length=250, unique=True, verbose_name='Название тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=250, unique=True, verbose_name='Слаг тега'),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='variationproduct',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата публикации'),
        ),
    ]