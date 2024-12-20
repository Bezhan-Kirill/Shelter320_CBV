from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from dogs.models import Category, Dog
from dogs.forms import DogForm


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


@login_required
def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Питомник - Все наши породы'
    }
    return render(request, 'dogs/categories.html', context)


@login_required
def category_dogs(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собаки породы - {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)

class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'

@login_required
def dogs_list_view(request):
    context = {
        'object_list': Dog.objects.all(),
        'title': 'Питомник - Все наши собаки',
    }
    return render(request, 'dogs/dogs.html', context)


@login_required
def dog_create_view(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog_object = form.save()
            dog_object.owner = request.user
            dog_object.save()
            form.save()
            return HttpResponseRedirect(reverse('dogs:list_dogs'))
    context = {
        'title': 'Добавление питомца',
        'form': DogForm(),
    }
    return render(request, 'dogs/create_update.html', context)


@login_required
def dog_detail_view(request, pk):
    context = {
        'object': Dog.objects.get(pk=pk),
        'title': 'Вы выбрали данного питомца'
    }
    return render(request, 'dogs/detail.html', context)


@login_required
def dog_update_view(request, pk):
    # dog_object = Dog.objects.get(pk=pk)
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:detail_dogs', args={pk: pk}))
    context = {
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    }
    return render(request, 'dogs/create_update.html', context)


@login_required
def dog_delete_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/delete.html', {
        'object': dog_object,
    })
