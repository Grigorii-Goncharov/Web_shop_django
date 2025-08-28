from django.core.cache import cache
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from .models import Products, Category
from django.views import View
from .forms import ProductsForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .services import get_products_by_category


class HomeView(ListView):
    """Отображает главную страницу каталога с продуктами.
    Показывает список продуктов в зависимости от прав пользователя:
    - Пользователи с правом 'catalog.can_unpublish_product' видят все товары.
    - Остальные пользователи видят только опубликованные товары.
    Также добавляет в контекст список всех категорий для навигации.
    Attributes:
        model (Model): Модель, используемая для получения данных — Products.
        context_object_name (str): Имя переменной в шаблоне для списка продуктов.
        template_name (str): Используемый шаблон.
    """
    model = Products
    context_object_name = "products"
    template_name = "catalog/home.html"

    def get_queryset(self):
        """Возвращает queryset продуктов, отфильтрованный по правам пользователя.
        Если пользователь имеет право 'catalog.can_unpublish_product', показываются все товары.
        В противном случае — только опубликованные. Результат кэшируется на 60 секунд.
        Returns:
            QuerySet: Отфильтрованный набор продуктов.
        """
        if self.request.user.is_authenticated and self.request.user.has_perm('catalog.can_unpublish_product'):
            cache_key = 'home_view_all_products'
            queryset = Products.objects.all()
        else:
            cache_key = 'home_view_published_only'
            queryset = Products.objects.filter(is_published=True)

        return cache.get_or_set(cache_key, queryset, 60)

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список всех категорий.
        Список категорий кэшируется на 60 секунд.
        Args:
            **kwargs: Дополнительные аргументы.
        Returns:
            dict: Контекст с продуктами и списком категорий.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = cache.get_or_set(
            'category_list',
            lambda: Category.objects.exclude(id__isnull=True),
            60
        )
        return context


class ProductDetailView(DetailView):
    """Отображает детальную информацию о продукте.
    Показывает полную информацию о продукте по его первичному ключу.
    В контекст добавляется список всех категорий для навигации.
    Attributes:
        model (Model): Модель продукта.
        context_object_name (str): Имя переменной в шаблоне.
        pk_url_kwarg (str): Имя параметра URL, содержащего первичный ключ.
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
    При сохранении устанавливает текущего пользователя как владельца продукта.
    После успешного создания перенаправляет на страницу созданного продукта.
    Attributes:
        model (Model): Модель продукта.
        form_class (Form): Форма для ввода данных.
    """

    model = Products
    form_class = ProductsForm

    def form_valid(self, form):
        """Присваивает текущего пользователя как владельца перед сохранением.
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
    Поддерживает переключение статуса публикации через POST-параметр 'toggle_publish'.
    После успешного редактирования перенаправляет на страницу продукта.
    Attributes:
        model (Model): Модель продукта.
        form_class (Form): Форма для редактирования.
        raise_exception (bool): Если True, вызывает 403 при отказе в доступе.
    """

    model = Products
    form_class = ProductsForm
    raise_exception = True

    def test_func(self):
        """Проверяет, является ли пользователь владельцем или имеет право на удаление.
        Используется для контроля доступа через UserPassesTestMixin.
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
        """Обрабатывает POST-запрос: редактирование или переключение публикации.
        Если в запросе присутствует параметр 'toggle_publish', переключает статус
        публикации продукта. Требует права 'catalog.can_unpublish_product'.
        Args:
            request (HttpRequest): POST-запрос.
        Returns:
            HttpResponse: Редирект или стандартный ответ обработки формы.
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
    После успешного удаления перенаправляет на главную страницу.
    Attributes:
        model (Model): Модель продукта.
        success_url (str): URL для перенаправления после удаления.
        raise_exception (bool): Если True, вызывает 403 при отказе в доступе.
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
    """Отображает и обрабатывает форму обратной связи на странице контактов.
    Обрабатывает GET-запрос (показ формы) и POST-запрос (приём данных).
    После отправки возвращает подтверждение.
    Attributes:
        template_name (str): Имя используемого шаблона.
    """

    template_name = "catalog/contacts.html"

    def get(self, request):
        """Отображает форму обратной связи.
        Args:
            request (HttpRequest): GET-запрос.
        Returns:
            HttpResponse: Отрендеренный шаблон с формой.
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


class ProductsByCategoryView(ListView):
    """Отображает продукты, относящиеся к указанной категории.
    Поведение зависит от прав пользователя:
    - Пользователи с правом 'catalog.can_unpublish_product' видят все товары.
    - Остальные — только опубликованные.
    Поддерживает пагинацию (по 10 товаров на страницу).
    Attributes:
        model (Model): Модель продуктов.
        context_object_name (str): Имя переменной в шаблоне.
        template_name (str): Имя шаблона.
        paginate_by (int): Количество товаров на странице.
    """

    model = Products
    context_object_name = "products"
    template_name = "catalog/products_by_category.html"
    paginate_by = 10

    def get_queryset(self):
        """Возвращает продукты указанной категории, отфильтрованные по правам.
        Args:
            category_id (int): ID категории из URL.
        Returns:
            QuerySet: Продукты указанной категории, отфильтрованные по статусу публикации.
        """
        category_id = self.kwargs["category_id"]
        products = get_products_by_category(category_id)

        if not self.request.user.has_perm("catalog.can_unpublish_product"):
            products = products.filter(is_published=True)

        return products

    def get_context_data(self, **kwargs):
        """Добавляет в контекст текущую категорию и список всех категорий.
        Args:
            **kwargs: Дополнительные аргументы.
        Returns:
            dict: Контекст с продуктами, текущей категорией и списком категорий.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs["category_id"]
        category = get_object_or_404(Category, pk=category_id)
        context["category"] = category
        context["categories"] = Category.objects.all()
        return context