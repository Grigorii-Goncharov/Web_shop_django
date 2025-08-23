from itertools import product

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse

import catalog
from .models import Products, Category
from django.views import View
from .forms import ProductsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class HomeView(ListView):
    """Представление для отображения главной страницы каталога.
    Отображает список продуктов на главной странице. Поведение зависит от прав пользователя:
    - Пользователи с правом 'catalog.can_unpublish_product' видят все товары (опубликованные и скрытые).
    - Обычные пользователи видят только опубликованные товары.
    Дополнительно в контекст передаётся список всех категорий для навигации или фильтрации.
    Attributes:
        model (Model): Модель, на основе которой строится список — Products.
        context_object_name (str): Имя переменной в шаблоне для списка объектов — 'products'.
        template_name (str): Путь к шаблону — 'catalog/home.html'.
    """

    model = Products
    context_object_name = "products"  # ← сейчас это object_list будет в 'product'
    template_name = "catalog/home.html"

    def get_queryset(self):
        """Фильтруем: только опубликованные для обычных, все — для модераторов"""
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return Products.objects.all()  # модератор видит всё
        else:
            return Products.objects.filter(
                is_published=True
            )  # остальные — только опубликованные

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """Представление для отображения детальной информации о продукте.
    Показывает информацию о конкретном продукте по его ID.
    """

    model = Products
    context_object_name = "product"
    pk_url_kwarg = "pk"  # совпадает с маршрутом <int:pk>, можно не указывать — по умолчанию и так 'pk'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список всех категорий.
        Args:
            **kwargs: Дополнительные аргументы.
        Returns:
            dict: Контекст с информацией о продукте и списком категорий.
        """
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context


class ProductsCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового продукта.
    Доступно только авторизованным пользователям.
    После успешного создания перенаправляет на страницу созданного продукта.
    """

    model = Products
    form_class = ProductsForm

    def get_success_url(self):
        """Определяет URL для перенаправления после успешного создания продукта.

        Returns:
            str: URL страницы созданного продукта.
        """
        return reverse("catalog:product", kwargs={"pk": self.object.pk})


class ProductsUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования существующего продукта.
    Доступно только авторизованным пользователям.
    После успешного редактирования перенаправляет на страницу продукта.
    """

    model = Products
    form_class = ProductsForm

    def get_success_url(self):
        return reverse("catalog:product", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        #  Если пришёл POST с флагом toggle_publish — просто переключаем статус
        if "toggle_publish" in request.POST:
            if not request.user.has_perm("catalog.can_unpublish_product"):
                return HttpResponseForbidden("У вас нет прав на публикацию")

            self.object.is_published = not self.object.is_published
            self.object.save()
            return redirect(self.get_success_url())

        #  Иначе — обычное поведение (редактирование формы)
        return super().post(request, *args, **kwargs)


class ProductsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Представление для удаления продукта.
    Доступно только авторизованным пользователям.
    После удаления перенаправляет на главную страницу.
    """

    model = Products
    success_url = reverse_lazy("catalog:home")
    permission_required = "catalog.delete_products"
    raise_exception = True


class ContactsView(View):
    """Представление для страницы контактов.
    Обрабатывает GET-запрос (отображение формы) и POST-запрос (обработка отправленных данных).
    """

    template_name = "catalog/contacts.html"

    def get(self, request):
        """Отображает форму обратной связи.
        Args:
            request (HttpRequest): GET-запрос от пользователя.
        Returns:
            HttpResponse: Отрендеренная страница с формой.
        """
        return render(request, self.template_name)

    def post(self, request):
        """Обрабатывает отправку формы обратной связи.
        Извлекает данные из формы (имя, email, сообщение) и возвращает ответ.
        Args:
            request (HttpRequest): POST-запрос с данными формы.
        Returns:
            HttpResponse: Сообщение об успешной отправке.
        """
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
