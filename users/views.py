import random
import string

from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_register_email, send_new_password


class UserRegisterView(CreateView):  # представление страницы создания пользователя
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'users/register_user.html'

    def form_valid(self, form):
        self.object = form.save()
        send_register_email(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):  # представление страницы создания пользователя
    template_name = 'users/login_user.html'
    form_class = UserLoginForm


class UserProfileView(UpdateView):  # представление страницы пользователя
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):  # представление страницы обновления пользователя
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):  # представление страницы смены пароля
    form_class = UserPasswordChangeForm
    template_name = 'users/change_password_user.html'
    success_url = reverse_lazy('users:profile_user')


class UserLogoutView(LogoutView):  # представление страницы выхода из акаунта
    template_name = 'users/logout_user.html'


class UserListView(ListView):  # представление страницы всех пользователей
    model = User
    paginate_by = 2
    extra_context = {
        'title': 'Питомник все наши заводчики'
    }
    template_name = 'users/users.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class UserViewProfileView(LoginRequiredMixin, DetailView):  # представление страницы пользователя
    model = User
    template_name = 'users/user_view_profile.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object = self.get_object()
        context_data[''] = f'{object.pk}'
        return context_data


def user_generate_new_password(request):  # функция генерирует новый пароль
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))  # создает пароль из 12 случайных букв и цифр
    request.user.set_password(new_password)  # устанавливает новый пароль и сохраняет
    request.user.save()
    send_new_password(request.user.email, new_password)  # отправляет новый пароль на почту
    return redirect(reverse('dogs:index'))  # возвращает на главную страницу
