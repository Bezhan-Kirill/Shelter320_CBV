from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):  # отправляет письмо на почту при регистрации
    send_mail(
        subject='Поздравляю с регистрацией',
        message='Вы успешно зарегестрировались на нашей платформе Web320Shelter, добро пожаловать!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

def send_new_password(email, new_password):  # отправляет письмо на почту при изменении пароля
    send_mail(
        subject='Вы успешно изменили пароль!',
        message=f'Ваш пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )