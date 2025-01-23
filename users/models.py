from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}

class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class User(AbstractUser):  # модель пользователя для базы данных
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=150, verbose_name='First Name', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='Last Name', default='Anonymous')
    phone = models.CharField(max_length=35, verbose_name='Phone number', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='Telegram Username', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='active')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    def get_email(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
        # abstract = True # данная модель станет абстрактным базовым классом
        # app_label = 'users' # если модель определена за пределами app., то таким образом можно ее к нему отнести
        # ordering = [-1] # изменение порядка полей в модели
        # proxy = True # модель будет рассматриваться как прокси модель
        # permissions = [] # добавляются группы пользователей которые могут изменять сущность данной модели
        # db_table = 'my_users' # перезаписать имя таблицы в БД
        # get_latest_by = 'birth_date' # возвращает последний объект по порядку возрастания (самый молодой пользователь)