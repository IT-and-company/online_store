# Generated by Django 4.2.4 on 2023-08-21 13:31

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите своё имя', max_length=250, verbose_name='Имя')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text='Введите номер телефона', max_length=15, region='RU', verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Обратный звонок',
                'verbose_name_plural': 'Обратные звонки',
                'ordering': ('phone',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите своё имя', max_length=250, verbose_name='Имя')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text='Введите номер телефона', max_length=15, region='RU', verbose_name='Телефон')),
                ('email', models.EmailField(help_text='Введите ваш email', max_length=254, verbose_name='Email')),
                ('address', models.CharField(max_length=250, verbose_name='Адрес доставки')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('phone',),
            },
        ),
    ]
