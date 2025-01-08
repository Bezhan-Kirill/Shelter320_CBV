from django.http import HttpResponseForbidden
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import UserRoles
from reviews.forms import ReviewForm


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Все отзывы о собаке'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListView(LoginRequiredMixin, ListView):
    model = Review
    extra_content = {
        'title': 'Неактивные отзыввы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(dog_pk=self.kwargs.get('pk'))
        queryset = queryset.filter(sign_of_review=False)
        return queryset


# class ReviewListView(LoginRequiredMixin, ListView):
#     model = Review
#     extra_context = {
#         'title': 'Все отзывы'
#     }
#     template_name = 'reviews/reviews_list.html'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter
