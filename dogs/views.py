from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, ParentForm, DogAdminForm
from users.models import UserRoles
from dogs.services import send_views_mail


def index(request):  # представление главной страницы
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class CategoryListView(LoginRequiredMixin, ListView):  # представление страницы списка породы
    model = Category
    extra_context = {
        'title': 'Питомник - Все наши породы'
    }
    template_name = 'dogs/categories.html'


class CategorySearchListView(LoginRequiredMixin, ListView):  # представление страницы поиска по породам
    model = Category
    template_name = 'dogs/categories.html'
    extra_context = {
        'title': 'Результаты поискового запроса',
    }

    def get_queryset(self):  # возвращает только тех собак где порода совпадает с запросом
        query = self.request.GET.get('q')
        object_list = Category.objects.filter(
            Q(name__icontains=query),
        )
        return object_list


class DogCategoryListView(ListView):  # представление страницы списка собак определенной породы
    model = Dog
    template_name = 'dogs/dogs.html'

    def get_queryset(self):  # выбирает разные породы собак
        queryset = super().get_queryset().filter(
            category_id=self.kwargs.get('pk'), is_active=True
        )

        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)

        return queryset


class DogListView(ListView):  # представление списка всех собак
    model = Dog
    paginate_by = 3
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):  # выбирает только активных собак
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivateListView(LoginRequiredMixin, ListView):  # представление списка неактивных собак
    model = Dog
    extra_context = {
        'title': 'Питомник - неактивные собаки',
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):  # выбирает только неактивных собак
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):  # представление поиска по кличкам
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Результаты поискового запроса',
    }

    def get_queryset(self): # выбирает собак по имени
        query = self.request.GET.get('q')
        object_list = Dog.objects.filter(
            Q(name__icontains=query), is_active=True,
        )
        return object_list


class DogCreateView(LoginRequiredMixin, CreateView):  # представление страницы добавления собаки
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        # if self.request.user.role != UserRoles.USER:
        #     raise PermissionDenied("У вас нет права доступа!")
        #     return HttpResponseForbidden("У вас нет права доступа") # только если ожидается перенаправление

        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):  # представление карточки собаки
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):  # возвращает словарь представляющий контекст шаблона
        context_data = super().get_context_data(**kwargs)
        object = self.get_object()
        context_data['title'] = f'{object.name} {object.category}'
        dog_object_increase = get_object_or_404(Dog, pk=object.pk)
        # if object.owner != self.request.user and self.request.user.role not in [UserRoles.ADMIN, UserRolesMODERATOR]:
        if object.owner != self.request.user:  # если пользователь не создатель собаки
            dog_object_increase.views_count()  # увеличивет количество просмотров на 1
        if object.owner:  # если пользователь создатель собаки
            object_owner_email = object.owner.email  # выбрать его почту
            if dog_object_increase.views % 100 == 0 and dog_object_increase.views != 0:  # если количество просмотров собаки больше 100
                send_views_mail(dog_object_increase.name, object_owner_email, dog_object_increase.views)  # отправить владельцу письмо на почту
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):  # представление страницы обновления собаки
    model = Dog
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])  # возвращает на карточку собаки

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)  # выбирает собаку для изменения
        # if self.object.owner != self.request.user and not self.request.user.is_staff:
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:  # если пользователь не создатель или админ доступ запрещен
            raise PermissionDenied()
        return self.object

    def get_form_class(self):
        dog_forms = {
            'admin': DogAdminForm,
            'moderator': DogForm,
            'user': DogForm,
        }
        user_role = self.request.user.role
        dog_form_class = dog_forms[user_role]
        return dog_form_class

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class DogDeleteView(PermissionRequiredMixin, DeleteView):  # представление страницы удаления собаки
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    permission_required = 'dogs:delete_dog'
    # dog.add_dog - PermissionRequiredMixin + CreateView
    # dog.change_dog - PermissionRequiredMixin + UpdateView
    # dog.view_dog - PermissionRequiredMixin + DetailView


def dog_toggle_activity(request, pk):  # переключает активных собак в неактивные и наоборот
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:list_dogs'))
