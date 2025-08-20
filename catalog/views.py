from django.shortcuts import render
from django.http import HttpResponse
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
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Products
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Products
    context_object_name = "product"
    pk_url_kwarg = "pk"  # совпадает с маршрутом <int:pk>, можно не указывать — по умолчанию и так 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()  # добавляем категории в контекст
        return context


class ProductsCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm

    def get_success_url(self):
        return reverse("catalog:product", kwargs={"pk": self.object.pk})


class ProductsUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    form_class = ProductsForm

    def get_success_url(self):
        return reverse("catalog:product", kwargs={"pk": self.object.pk})


class ProductsDeleteView(LoginRequiredMixin, DeleteView):
    model = Products
    success_url = reverse_lazy("catalog:home")


# ФУНКЦИЯ ОТОБРАЖЕНИЯ И ОТПРАВКИ ФОРМЫ ЗАПРОСА
class ContactsView(View):
    template_name = "catalog/contacts.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
