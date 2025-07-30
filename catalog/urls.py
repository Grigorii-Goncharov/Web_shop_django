from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name="home"),  # главная страница
    path('contacts/', views.contacts, name="contacts"),
    path('product/<int:pk>/', views.product, name="product"),

]
