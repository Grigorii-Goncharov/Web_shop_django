from .models import Products, Category


def get_products_by_category(category_id):
    """
    Возвращает список продуктов, относящихся к указанной категории.
    Если пользователь — модератор (имеет право can_unpublish_product), показывает все товары.
    Иначе — только опубликованные.

    Args:
        category_id (int): ID категории.

    Returns:
        QuerySet: Отфильтрованные продукты в заданной категории.
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Products.objects.none()

    if hasattr(category, "products"):
        products = category.products.all()
    else:
        products = Products.objects.filter(category=category)

    return products
