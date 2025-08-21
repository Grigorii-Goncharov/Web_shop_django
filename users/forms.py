from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания профиля"""

    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "phone", "country", "image"]

    def clean_email(self):
        """Метод проверки на предмет совпадения почтового адреса в базе. Должен быть уникальным"""
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля, без смены паролья"""

    class Meta:
        model = User
        fields = ["email", "phone", "country", "image"]

    def clean_phone(self):
        """Метод проверки на номера телефона - должен быть числовым!"""
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone

    def clean_email(self):
        """Метод проверки на email на корректность и его уникальность в Базе данных"""
        email = self.cleaned_data.get("email")
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError("Введите корректный email-адрес.")

            # Проверка уникальности email (кроме текущего пользователя)
            if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise forms.ValidationError("Этот email уже используется.")
        return email
