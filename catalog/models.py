from django.db import models

from users.models import User


class Category(models.Model):
    """Модель категории товара.
    Используется для группировки продуктов по категориям (например, 'Электроника', 'Одежда').
    Attributes:
        name (CharField): Название категории (до 100 символов).
        description (TextField): Описание категории (до 300 символов).
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите название категории, например: 'Электроника', 'Мебель'.",
    )
    description = models.TextField(
        max_length=300,
        verbose_name="Описание",
        help_text="Краткое описание категории (до 300 символов).",
    )

    def __str__(self):
        """Возвращает строковое представление объекта Category.
        Returns:
            str: Название категории.
        """
        return self.name

    class Meta:
        """Метакласс для настройки отображения модели в административной панели."""

        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]  # Сортировка по названию в алфавитном порядке


class Products(models.Model):
    """Модель продукта.
    Представляет товар в каталоге с названием, описанием, изображением,
    категорией, ценой и датами создания/обновления.
    Attributes:
        name (CharField): Название продукта.
        description (TextField): Описание продукта.
        image (ImageField): Изображение товара (необязательное).
        category (ForeignKey): Связь с моделью Category.
        purchase_price (IntegerField): Цена товара (в рублях или другой валюте).
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего обновления.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите название товара (например, 'Смартфон Samsung').",
    )
    description = models.TextField(
        max_length=300,
        verbose_name="Описание",
        help_text="Краткое описание товара (до 300 символов).",
    )
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Изображение",
        help_text="Загрузите изображение товара (опционально).",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",  # Исправлено: лучше использовать lowercase имена
        verbose_name="Категория",
        help_text="Выберите категорию, к которой относится товар.",
    )
    purchase_price = models.IntegerField(
        verbose_name="Цена за покупку",
        help_text="Укажите цену товара (не может быть отрицательной).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name="Дата создания",
        help_text="Дата и время автоматического создания записи.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        verbose_name="Дата последнего обновления",
        help_text="Автоматически обновляется при каждом изменении.",
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Указывает, опубликован ли товар на сайте. По умолчанию — не опубликован.",
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="продукты пользователя")

    def __str__(self):
        """Возвращает строковое представление объекта Products.
        Returns:
            str: Название товара и его цена.
        """
        return f"{self.name} — {self.purchase_price} ₽"

    class Meta:
        """Метакласс для настройки отображения модели в административной панели."""

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = [
            "name",
            "purchase_price",
        ]  # Сортировка сначала по имени, затем по цене
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]
