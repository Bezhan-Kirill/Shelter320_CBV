from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from dogs.models import Category


def get_categories_cache():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list


def send_views_mail(dog_object, owner_email, views_count): # функция отправляет письмо владельцу когда его собака набирает 100 просмотров
    send_mail(
        subject=f'{views_count} просмотров {dog_object}', # Тема письма
        message=f'{views_count} просмотров {dog_object}', # Содержание письма
        from_email=settings.EMAIL_HOST_USER, # отправитель
        recipient_list=[owner_email, ] # получатель
    )
