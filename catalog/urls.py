from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='hone'),
    path('home.html', views.home, name='home'),
    path('contacts.html', views.contacts, name='contacts'),
]
