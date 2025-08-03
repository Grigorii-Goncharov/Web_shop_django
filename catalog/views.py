from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Products, Category


def home(request):
    products = Products.objects.all()
    category = Category.objects.all()
    context = {'products': products, 'category': category}
    return render(request, template_name="home.html", context=context)


# def contacts(request):
#     return render(request, template_name="contacts.html")

def product(request, pk):
    '''Загрузка страницы с конкретным продуктом по первичному ключу'''
    product = get_object_or_404(Products, pk=pk)
    category = Category.objects.all()
    context = {'product': product, 'category': category}
    return render(request, 'product.html', context=context)


# ФУНКЦИЯ ОТОБРАЖЕНИЯ И ОТПРАВКИ ФОРМЫ ЗАПРОСА
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'contacts.html')
