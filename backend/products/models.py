from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


class Category(models.Model):
    """Категории товаров

    Товары делятся на категории: «Мягкая мебель», «Кухни», «Спальни», "Гостиные",
    "Прихожие", "Детская мебель".so
    Список категорий может быть расширен администратором.
    """
    name = models.CharField(
        'Название категории',
        max_length=settings.MAX_LENGTH_1
    )
    slug = models.SlugField(
        'Слаг категории',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:settings.MAX_LENGTH_3]


class Type(models.Model):
    """Тип товара

    Товары делятся на типы: "Диваны", "Кресла" и т.д
    """
    name = models.CharField(
        'Название жанра',
        max_length=settings.MAX_LENGTH_1
    )
    slug = models.SlugField(
        'Слаг жанра',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:settings.MAX_LENGTH_3]


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        unique=True,
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите тег'
    )
    color = models.CharField(
        'Цвет тега',
        unique=True,
        max_length=settings.MAX_LENGTH_2,
        help_text='Укажите цвет тега'
    )
    slug = models.SlugField(
        'Слаг тега',
        unique=True,
        max_length=settings.MAX_LENGTH_1
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Size(models.Model):
    length = models.PositiveSmallIntegerField(
        'длина',
    )
    width = models.PositiveSmallIntegerField(
        'ширина',
    )
    height = models.PositiveSmallIntegerField(
        'ширина',
    )

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'размеры'

    def __str__(self):
        return f'{self.length} х {self.width} х {self.height} см'


class Product(models.Model):
    name = models.CharField(
        'Название товара',
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите название товара'
    )
    image = models.ImageField(
        'Фото товара',
        upload_to='product/',
        help_text='Загрузите фото товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    sale = models.IntegerField(
        'Скидка в процентах',
        blank=True,
        default=0
    )
    text = models.TextField(
        'Описание товара',
        help_text='Напишите описание товара'
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        verbose_name='Тег товара',
        related_name='colour'
    )
    category = models.ManyToManyField(
        Category,
        related_name='category',
        verbose_name='Категория товара'
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип товара'
    )
    size = models.ManyToManyField(
        Size,
        related_name='size',
        verbose_name='Размер товара'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
