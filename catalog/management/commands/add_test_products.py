from django.core.management.base import BaseCommand
from catalog.models import Products, Category


class Command(BaseCommand):
    help = 'Add test products in database'

    def handle(self, *args, **kwargs):
        # чистим все товары из БД
        Products.objects.all().delete()

        category1, _ = Category.objects.get_or_create(name='Гаджеты')
        category2, _ = Category.objects.get_or_create(name='Бытовая техника')
        category3, _ = Category.objects.get_or_create(name='Атомобиль')

        products = [
            {"name": "Iphone 16", "description": "128 Гб", "image": "", "category": category1, "purchase_price": 55000},
            {"name": "Iphone 16 Pro", "description": " 128 Гб", "image": "", "category": category1,
             "purchase_price": 60000},
            {"name": "Iphone 16 Pro MAX", "description": "Плита", "image": "", "category": category1,
             "purchase_price": 64000},

            {"name": "Gorenie", "description": "Вытяжка", "image": "", "category": category2, "purchase_price": 2000},
            {"name": "Bosh", "description": " Cтиральная машина", "image": "", "category": category2,
             "purchase_price": 35000},
            {"name": "electrolux", "description": "Плита", "image": "", "category": category2, "purchase_price": 12000},

            {"name": "BMW", "description": "Автомобиль из баварии>", "image": "", "category": category3,
             "purchase_price": 1520000},
            {"name": "AUDI", "description": " Автомобиль из германии", "image": "", "category": category3,
             "purchase_price": 1350000},
            {"name": "Mersedes", "description": "Автомобиль из германии", "image": "", "category": category3,
             "purchase_price": 120000},
        ]

        for product in products:
            product, created = Products.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Товар {product.name} успешно добавлен в базу!'))
            else:
                self.stdout.write(self.style.WARNING(f'Выбранные товары {product.name} уже имеется в базе!'))
