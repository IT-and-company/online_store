from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from smart_selects.db_fields import ChainedForeignKey

from PIL import Image

User = get_user_model()


class CategoryType(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.MAX_LENGTH_1
    )
    slug = models.SlugField(
        'Слаг',
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:settings.MAX_LENGTH_3]


class Category(CategoryType):
    """Категории товаров

    Товары делятся на категории: «Мягкая мебель», «Кухни», «Спальни»,
    "Гостиные", "Прихожие", "Детская мебель".so
    Список категорий может быть расширен администратором.
    """

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Type(CategoryType):
    """Тип товара

    Товары делятся на типы: "Диваны", "Кресла" и т.д
    """
    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class ProductModel(CategoryType):
    """
    Модель товара
    """
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип товара'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class ColorTag(models.Model):
    color_name = models.CharField(
        'Название цвета',
        unique=True,
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите тег'
    )
    hex = models.CharField(
        'Код цвета',
        unique=True,
        max_length=settings.MAX_LENGTH_2,
        help_text='Укажите цвет тега'
    )
    slug = models.SlugField(
        'Слаг цвета',
        unique=True,
        max_length=settings.MAX_LENGTH_1
    )

    class Meta:
        verbose_name = 'Тег цвета'
        verbose_name_plural = 'Теги цвета'

    def __str__(self):
        return self.color_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.color_name)
        return super().save(*args, **kwargs)


class Size(models.Model):
    length = models.PositiveSmallIntegerField(
        'длина',
    )
    width = models.PositiveSmallIntegerField(
        'ширина',
    )
    height = models.PositiveSmallIntegerField(
        'высота',
    )

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return f'{self.length} х {self.width} х {self.height} см'


class Product(models.Model):
    name = models.CharField(
        'Название товара',
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите название товара'
    )
    text = models.TextField(
        'Описание товара',
        blank=True,
        help_text='Напишите описание товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория товара'
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип товара'
    )
    model = ChainedForeignKey(
        ProductModel,
        related_name='model',
        verbose_name='Модель товара',
        chained_field="type",
        chained_model_field="type",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name', 'type', ],
            name='unique_type')
        ]

    def __str__(self):
        return self.name


class Specification(models.Model):
    article_number = models.CharField(
        'Артикул товара',
        blank=True,
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите артикул товара'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        null=True,
        related_name='size_in_specific',
        verbose_name='Размер товара'
    )
    model = models.CharField(
        'Тип модели',
        blank=True,
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите тип товара'
    )
    materials = models.CharField(
        'Материалы',
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите материалы товара'
    )
    manufacturer = models.CharField(
        'Производитель',
        blank=True,
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите Производителя'
    )

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return (f'{self.article_number}, '
                f'{self.size}, '
                f'{self.model}, '
                f'{self.materials}, '
                f'{self.manufacturer}')


class Picture(models.Model):
    image = models.ImageField(
        'Фото товара',
        upload_to='product/%Y/%m/%d',
        blank=True,
        null=True,
        help_text='Загрузите фото товара'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.image.name.split("/")[-1]}'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 450 or img.width > 850:
            output_size = (450, 850)
            img.thumbnail(output_size)
            img.save(self.image.path)


class VariationProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='Товары'
    )
    image = models.ManyToManyField(
        Picture,
        verbose_name='Фотографии'
    )
    price = models.IntegerField(
        'Цена',
        blank=True,
        default=0
    )
    sale = models.IntegerField(
        'Скидка в процентах',
        blank=True,
        default=0
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='products',
        verbose_name='Размер товара'
    )
    color_tag = models.ForeignKey(
        ColorTag,
        on_delete=models.SET_NULL,
        null=True,
        db_index=True,
        verbose_name='Цвет товара',
        related_name='products'
    )
    specification = models.ForeignKey(
        Specification,
        null=True,
        on_delete=models.SET_NULL,
        related_name='specification'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return (f'{self.product.name}: '
                f'{self.price} '
                f'{self.size} '
                f'{self.specification}')


class FavoriteBasket(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        VariationProduct,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.product}'


class Favorite(FavoriteBasket):
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'product'],
            name='unique_favorite')
        ]
        default_related_name = 'favorite'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
