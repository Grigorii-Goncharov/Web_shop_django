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
    категорией, ценой, статусом публикации и владельцем.

    Используется для хранения информации о товарах, доступных в интернет-магазине.
    Поддерживает привязку к категории, загрузку изображения, указание цены,
    а также управление публикацией и правами доступа через владельца и разрешения.

    Attributes:
        name (CharField): Название товара (до 100 символов).
        description (TextField): Краткое описание товара (до 300 символов).
        image (ImageField): Изображение товара; может быть пустым.
        category (ForeignKey): Связь с моделью Category; при удалении категории
                              все связанные товары также удаляются.
        purchase_price (IntegerField): Цена товара в рублях (или другой валюте).
        created_at (DateTimeField): Дата и время создания записи (устанавливается автоматически).
        updated_at (DateTimeField): Дата и время последнего обновления (обновляется автоматически).
        is_published (BooleanField): Статус публикации товара.
                                    Если True — товар отображается на сайте.
                                    По умолчанию False (не опубликован).
        owner (ForeignKey): Владелец товара — пользователь из модели User.
                           Может быть пустым (null=True, blank=True).
                           При удалении пользователя все его товары удаляются (CASCADE).

    Permissions:
        can_unpublish_product: Разрешение, позволяющее снимать товар с публикации.
                               Назначается через группу или пользователя в админке.

    Example:
        Продукт: "Смартфон Iphone16 256GB" — 72000 ₽, категория "Электроника",
        опубликован: Да, владелец: user1@example.com.

    Note:
        Для фильтрации опубликованных товаров используйте:
        Products.objects.filter(is_published=True)
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

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owners_product",
        verbose_name="продукты пользователя",
        null=True,
        blank=True,
    )

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
