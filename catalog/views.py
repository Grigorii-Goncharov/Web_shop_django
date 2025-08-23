from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .models import Products, Category
from django.views import View
from .forms import ProductsForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomeView(ListView):
    """Представление главной страницы каталога.

    Отображает список продуктов. Поведение зависит от прав пользователя:
    - Пользователи с правом 'catalog.can_unpublish_product' видят все товары.
    - Остальные пользователи видят только опубликованные товары.
    В контекст также передаётся список всех категорий для навигации или фильтрации.
    Attributes:
        model (Model): Модель, на основе которой строится список — Products.
        context_object_name (str): Имя переменной в шаблоне для списка продуктов.
        template_name (str): Путь к шаблону.
    """

    model = Products
    context_object_name = "products"
    template_name = "catalog/home.html"

    def get_queryset(self):
        """Возвращает queryset продуктов в зависимости от прав пользователя.
        Returns:
            QuerySet: Все продукты (для модераторов) или только опубликованные.
        """
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return Products.objects.all()
        return Products.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список всех категорий.
        Args:
            **kwargs: Дополнительные аргументы.
        Returns:
            dict: Контекст с продуктами и списком категорий.
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """Представление детальной информации о продукте.
    Отображает полную информацию о товаре по его ID.
    В контекст добавляется список всех категорий для навигации.
    """

    model = Products
    context_object_name = "product"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список всех категорий.
        Args:
            **kwargs: Дополнительные аргументы.
        Returns:
            dict: Контекст с информацией о продукте и списком категорий.
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductsCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового продукта.

    Доступно только авторизованным пользователям.
    При создании автоматически устанавливает текущего пользователя как владельца.
    После успешного создания перенаправляет на страницу созданного продукта.
    Attributes:
        model (Model): Модель продукта.
        form_class (Form): Форма для ввода данных.
    """

    model = Products
    form_class = ProductsForm

    def form_valid(self, form):
        """Устанавливает текущего пользователя как владельца перед сохранением.
        Args:
            form (ProductsForm): Форма с валидированными данными.
        Returns:
            HttpResponse: Результат обработки формы (перенаправление).
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Определяет URL для перенаправления после успешного создания.
        Returns:
            str: URL страницы созданного продукта.
        """
        return reverse("catalog:product", kwargs={"pk": self.object.pk})


class ProductsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление для редактирования продукта.
    Доступно владельцу продукта или пользователям с правом 'catalog.delete_products'.
    Поддерживает переключение статуса публикации при отправке специального POST-параметра.
    После успешного редактирования перенаправляет на страницу продукта.
    """

    model = Products
    form_class = ProductsForm
    raise_exception = True

    def test_func(self):
        """Проверяет, является ли пользователь владельцем или имеет право на удаление.
        Используется UserPassesTestMixin для проверки доступа.
        Returns:
            bool: True, если пользователь — владелец или имеет право.
        """
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm("catalog.delete_products")

    def get_success_url(self):
        """Определяет URL для перенаправления после успешного редактирования.
        Returns:
            str: URL страницы продукта.
        """
        return reverse("catalog:product", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос: либо редактирование, либо переключение публикации.
        Если в запросе есть параметр 'toggle_publish', переключает статус публикации.
        Требует права 'catalog.can_unpublish_product'.
        Args:
            request (HttpRequest): POST-запрос.
        Returns:
            HttpResponse: Редирект или результат стандартной обработки.
        """
        self.object = self.get_object()

        if "toggle_publish" in request.POST:
            if not request.user.has_perm("catalog.can_unpublish_product"):
                return HttpResponseForbidden("У вас нет прав на публикацию/снятие с публикации.")
            self.object.is_published = not self.object.is_published
            self.object.save()
            return redirect(self.get_success_url())

        return super().post(request, *args, **kwargs)


class ProductsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Представление для удаления продукта.
    Доступно владельцу продукта или пользователям с правом 'catalog.delete_products'.
    После удаления перенаправляет на главную страницу.
    """

    model = Products
    success_url = reverse_lazy("catalog:home")
    raise_exception = True

    def test_func(self):
        """Проверяет, является ли пользователь владельцем или имеет право на удаление.
        Returns:
            bool: True, если пользователь — владелец или имеет право.
        """
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm("catalog.delete_products")


class ContactsView(View):
    """Представление страницы контактов.
    Обрабатывает GET-запрос (отображение формы) и POST-запрос (обработка данных).
    """

    template_name = "catalog/contacts.html"

    def get(self, request):
        """Отображает форму обратной связи.
        Args:
            request (HttpRequest): GET-запрос.
        Returns:
            HttpResponse: Отрендеренный шаблон формы.
        """
        return render(request, self.template_name)

    def post(self, request):
        """Обрабатывает отправку формы обратной связи.
        Извлекает имя, email и сообщение из POST-данных и возвращает подтверждение.
        Args:
            request (HttpRequest): POST-запрос с данными формы.
        Returns:
            HttpResponse: Сообщение об успешной отправке.
        """
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")