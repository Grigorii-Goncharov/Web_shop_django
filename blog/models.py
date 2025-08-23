from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    """Модель для хранения блог-постов.
    Представляет собой запись в блоге с заголовком, содержанием, превью,
    датой создания, флагом публикации и счётчиком просмотров.
    Attributes:
        title (CharField): Заголовок поста (до 200 символов).
        content (TextField): Основное содержание поста.
        preview (ImageField): Изображение-превью поста (необязательное).
        created_at (DateTimeField): Дата и время создания поста.
        is_published (BooleanField): Флаг, определяющий, опубликован ли пост.
        views_count (PositiveIntegerField): Счётчик количества просмотров поста.
    """

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog_previews/",
        blank=True,
        null=True,
        verbose_name="Изображение (превью)",
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]  #  "-" обратный порядок сортировки

    def __str__(self):
        return self.title
