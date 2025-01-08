from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from reviews.models import Review


class CategoryListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Все отзывы о собаке'
    }
    template_name = 'reviews/review.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dog_pk=self.kwargs.get('pk'))
        queryset = queryset.filter(sign_of_review=True)

        return queryset


class UnactiveDogReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_content = {
        'titel': 'Неактивные отзыввы'
    }
    template_name = 'reviews/review.html'

    def get_quertset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dog_pk=self.kwargs.get('pk'))
        queryset = queryset.filter(sign_of_review=False)

        return queryset


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Все отзывы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter
