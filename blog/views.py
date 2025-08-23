# views.py
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from .models import BlogPost


class BlogPostListView(ListView):
    """Представление для отображения списка опубликованных блог-постов.
    Показывает только опубликованные записи с пагинацией.
    """

    model = BlogPost
    context_object_name = "posts"
    paginate_by = 4  # Количество постов на странице

    def get_queryset(self):
        """Возвращает queryset только опубликованных блог-постов.
        Returns:
            QuerySet: Список опубликованных записей BlogPost.
        """
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Представление для отображения детальной информации о блог-посте.
    Увеличивает счётчик просмотров при каждом открытии поста.
    """

    model = BlogPost
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Получает объект поста и увеличивает счётчик просмотров.
        Args:
            queryset (QuerySet, optional): Набор объектов. По умолчанию None.
        Returns:
            BlogPost: Объект блог-поста с увеличенным счётчиком просмотров.
        """
        object_blog = super().get_object(queryset)
        object_blog.views_count += 1
        object_blog.save(
            update_fields=["views_count"]
        )  # Оптимизация: обновляем только одно поле
        return object_blog


class BlogPostCreateView(CreateView):
    """Представление для создания нового блог-поста.
    Поля формы: заголовок, содержание, изображение-превью.
    После успешного создания перенаправляет на список постов.
    """

    model = BlogPost
    fields = ["title", "content", "preview"]
    success_url = reverse_lazy("blog:list")


class BlogPostUpdateView(UpdateView):
    """Представление для редактирования существующего блог-поста.
    Поля формы: заголовок, содержание, превью.
    После сохранения перенаправляет на страницу редактированного поста.
    """

    model = BlogPost
    fields = ["title", "content", "preview"]

    def get_success_url(self):
        """Определяет URL для перенаправления после успешного редактирования.
        Returns:
            str: URL детальной страницы поста.
        """
        return reverse("blog:detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Представление для подтверждения и удаления блог-поста.
    После удаления перенаправляет на список всех постов.
    """

    model = BlogPost
    success_url = reverse_lazy("blog:list")
