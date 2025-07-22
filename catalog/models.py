from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=300, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length = 300, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE,related_name='Категория')
    purchase_price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.name} {self.purchase_price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', 'purchase_price']


