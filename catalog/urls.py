from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig

from .views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    ProductsCreateView,
    ProductsDeleteView,
    ProductsUpdateView,
)

app_name = CatalogConfig.name


urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # главная страница
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="product"),
    path("product/create/", ProductsCreateView.as_view(), name="create"),
    path("product/update/<int:pk>/", ProductsUpdateView.as_view(), name="update"),
    path("product/delete/<int:pk>/", ProductsDeleteView.as_view(), name="delete"),
]
