from django import template

from django.conf import settings
register = template.Library()

# @register.filter()
# def media_filter(path):
#     if path:
#         return f'/media/{path}'
#     return '#'

@register.filter
def media_filter(path):
    '''Фильтр, путь медиа от папки media/имя_файла'''
    if path:
        # Используем настоящий MEDIA_URL
        return f"{settings.MEDIA_URL}{path}".replace('//', '/')
    return "#"
