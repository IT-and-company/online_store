from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

User = get_user_model()


class CategoryType(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=settings.MAX_LENGTH_1
    )
    slug = models.SlugField(
        'Слаг категории',
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:settings.MAX_LENGTH_3]


class Category(CategoryType):
    """Категории товаров

    Товары делятся на категории: «Мягкая мебель», «Кухни», «Спальни», "Гостиные",
    "Прихожие", "Детская мебель".so
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
        'высота',
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
    text = models.TextField(
        'Описание товара',
        blank=True,
        help_text='Напишите описание товара'
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
    size = models.ManyToManyField(
        Size,
        related_name='size_in_specific',
        verbose_name='Размер товара'
    )
    type = models.CharField(
        'Тип механизмов',
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите тип товара'  #Например угловой, модульный и т.д.
    )
    materials = models.CharField(
        'Материлы',
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите материлы товара'
    )
    manufacturer = models.CharField(
        'Производитель',
        max_length=settings.MAX_LENGTH_1,
        help_text='Введите Производителя'
    )

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return (f'{self.article_number}, '
                f'{self.size}, '
                f'{self.type}, '
                f'{self.materials}, '
                f'{self.manufacturer}')


class Image(models.Model):
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


class VariationProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='Товары'
    )
    image = models.ManyToManyField(
        Image,
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
    size = models.ManyToManyField(
        Size,
        blank=True,
        related_name='size',
        verbose_name='Размер товара'
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        verbose_name='Цвет товара',
        related_name='colour'
    )
    specification = models.ForeignKey(
        Specification,
        null=True,
        on_delete=models.SET_NULL,
        related_name='specification'
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return (f'{self.product.name}: '
                f'{self.price} '
                f'{self.size} '
                f'{self.specification}')


class FavoriteBasket(models.Model):
    user = models.ForeignKey(
        User,
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


class Basket(FavoriteBasket):
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        default_related_name = 'basket'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
