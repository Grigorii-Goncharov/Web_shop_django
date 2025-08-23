# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Products

FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар",
]


class ProductsForm(forms.ModelForm):
    """Форма для создания и редактирования продукта на основе модели Products.
    Включает валидацию полей:
    - Проверка на запрещённые слова в названии и описании.
    - Ограничения на формат и размер изображения.
    - Проверка, что цена не отрицательная.
    Дополнительно настраивает HTML-атрибуты полей для интеграции с Bootstrap.
    """

    class Meta:
        """Метакласс, определяющий модель и поля формы."""

        model = Products
        fields = [
            "name",
            "description",
            "image",
            "category",
            "purchase_price",
        ]

    def __init__(self, *args, **kwargs):
        """Инициализация формы и настройка атрибутов полей для отображения.
        Добавляет CSS-классы и placeholder'ы для улучшения внешнего вида в шаблоне.
        Args:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.
        """
        super(ProductsForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя товара"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Описание продукта"}
        )
        self.fields["image"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Изображение"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Категория товара"}
        )
        self.fields["purchase_price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Цена товара"}
        )

    def clean_name(self):
        """Проверяет, что в названии продукта отсутствуют запрещённые слова.
        Регистронезависимая проверка. Если найдено совпадение — вызывает ValidationError.
        Returns:
            str: Очищенное значение поля name.
        Raises:
            ValidationError: Если название содержит запрещённое слово.
        """
        name = self.cleaned_data.get("name")
        if name:
            for word in FORBIDDEN_WORDS:
                if word.lower() in name.lower():
                    raise ValidationError(
                        f'Введенное слово "{word}" запрещено для использования в поле наименования'
                    )
        return name

    def clean_description(self):
        """Проверяет, что в описании продукта отсутствуют запрещённые слова.
        Регистронезависимая проверка. Если найдено совпадение — вызывает ValidationError.
        Returns:
            str: Очищенное значение поля description.
        Raises:
            ValidationError: Если описание содержит запрещённое слово.
        """
        description = self.cleaned_data.get("description")
        if description:
            for word in FORBIDDEN_WORDS:
                if word.lower() in description.lower():
                    raise ValidationError(
                        f'Введенное слово "{word}" запрещено для использования в поле описания'
                    )
        return description

    def clean_image(self):
        """Проверяет формат и размер загружаемого изображения.
        Допустимые форматы: .png, .jpg, .jpeg.
        Максимальный размер: 5 МБ.
        Returns:
            ImageFieldFile: Очищенное значение поля image.
        Raises:
            ValidationError: Если формат недопустим или размер превышает лимит.
        """
        image = self.cleaned_data.get("image")
        if image:
            if not image.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise ValidationError(
                    "Некорректный формат файла. Допустимые: PNG, JPG, JPEG."
                )
            if image.size > 5 * 1024 * 1024:  # 5 МБ
                raise ValidationError("Размер файла не может превышать 5 МБ.")
        return image

    def clean_purchase_price(self):
        """Проверяет, что стоимость товара не является отрицательной.
        Returns:
            Decimal: Очищенное значение поля purchase_price.
        Raises:
            ValidationError: Если цена меньше нуля.
        """
        price = self.cleaned_data.get("purchase_price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price
