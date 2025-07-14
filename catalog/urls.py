from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import home, contacts

app_name = CatalogConfig.name

urlpatterns = [
    #path('', include('catalog.urls', namespace="catalog")),
    path('', home, name="home"),
    path('', contacts, name="contacts"),

]