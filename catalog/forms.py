# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Products

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "name",
            "description",
            "image",
            "category",
            "purchase_price",
        ]

    def __init__(self, *args, **kwargs):
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
        name = self.cleaned_data.get("name")
        if name:
            for word in FORBIDDEN_WORDS:
                if word.lower() in name.lower():
                    raise ValidationError(
                        f'Введенное слово "{word}" запрещено для использования в поле наименования'
                    )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            for word in FORBIDDEN_WORDS:
                if word.lower() in description.lower():
                    raise ValidationError(
                        f'Введенное слово "{word}" запрещено для использования в поле описания'
                    )
        return description

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if not image.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise ValidationError("Некорректный формат файла")
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер не может превышать более 5 Мбайт")
        return image

    def clean_purchase_price(self):
        price = self.cleaned_data.get("purchase_price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price
