from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='hone'),
    path('contacts/', views.contacts, name='contacts'),
]
