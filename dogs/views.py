from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, ParentForm
from users.models import UserRoles

def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Питомник - Все наши породы'
    }
    template_name = 'dogs/categories.html'


class DogCategoryListView(ListView):
    model = Dog
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            category_id=self.kwargs.get('pk'),
        )

        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)

        return queryset


class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivateListView(LoginRequiredMixin, ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - неактивные собаки',
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:dogs')

    def form_valid(self, form):
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied("У вас нет права доступа!")
            # return HttpResponseForbidden("У вас нет права доступа") # только если ожидается перенаправление
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'dogs/detail.html'


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        # if self.object.owner != self.request.user and not self.request.user.is_staff:
        if self.object.owner != self.request.user and self.request.user.role !=UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent,  form=ParentForm, extra=1)
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


class DogDeleteView(PermissionRequiredMixin ,DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    permission_required = ('dogs.delete/dog')
    # dog.add_dog - PermissionRequiredMixin + CreateView
    # dog.change_dog - PermissionRequiredMixin + UpdateView
    # dog.view_dog - PermissionRequiredMixin + DetailView


def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:list_dogs'))