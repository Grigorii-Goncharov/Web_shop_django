from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def home(request):
    return render(request, template_name="home.html")


# def contacts(request):
#     return render(request, template_name="contacts.html")

# ФУНКЦИЯ ОТОБРАЖЕНИЯ И ОТПРАВКИ ФОРМЫ ЗАПРОСА
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'contacts.html')
