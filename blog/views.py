# views.py
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    # template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 4  # Опционально: пагинация

    def get_queryset(self):
        # Только опубликованные посты
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    # template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        object_blog = super().get_object(queryset)
        object_blog.views_count += 1
        object_blog.save(update_fields=['views_count'])
        return object_blog


class BlogPostCreateView(CreateView):
    model = BlogPost
    # template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview']
    success_url = reverse_lazy('blog:list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    # template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview']
    #success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:detail', kwargs = {'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    # template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')