from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import UserRoles
from reviews.forms import ReviewForm
from reviews.utils import slug_generator


class ReviewListView(LoginRequiredMixin, ListView):  # представление для страницы списка всех отзывов
    model = Review  # имя модели
    paginate_by = 2  # пагинация по два отзыва на страницу
    extra_context = {
        'title': 'Все отзывы о собаке' # добавляет заголовок на страницу
    }
    template_name = 'reviews/reviews_list.html'  # имя шаблона

    def get_queryset(self):  # выбирает все отзывы где sign_of_review истино
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListView(LoginRequiredMixin, ListView):  # представление для страницы списка всех неактивных отзывов
    model = Review  # имя модели
    extra_content = {
        'title': 'Неактивные отзывы'  # добавляет заголовок на страницу
    }
    template_name = 'reviews/reviews_list.html'  # имя шаблона

    def get_queryset(self):  # выбирает только отзывы где sign_of_review ложно
        queryset = super().get_queryset()
        # queryset = queryset.filter(dog_pk=self.kwargs.get('pk'))
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class ReviewCreateView(CreateView):  # представление создания отзыва
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'

    def form_valid(self, form):  # создает для отзыва уникальный slug указывает создателя отзыва
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden()
        self.object = form.save()
        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ReviewDetailView(LoginRequiredMixin, DetailView):  # представление карточки отзыва
    model = Review
    template_name = 'reviews/review_detail.html'


class ReviewUpdateView(UpdateView):  # представление страницы обновления отзыва
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'

    def get_success_url(self):
        return reverse('reviews:detail_review', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and self.request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:  # если пользователь не создатель отзыва или админ/модератор
            raise PermissionDenied()  # в доступе будет отказано
        return self.object


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):  # представление страницы удаления отзыва
    model = Review
    template_name = 'reviews/review_delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        return reverse('reviews:list_reviews')  # возвращает на страницу отзывов


def review_toggle_activity(request, slug):  # функция переводит активные отзывы в неактивные и наоборот
    review_item = get_object_or_404(Review, slug=slug)  # выбирает отзыв по уникальному slug
    if review_item.sign_of_review:  # если sign_of review истино
        review_item.sign_of_review = False  # переводит его в ложное
        review_item.save()  # сохраняет в базе данных
        return redirect(reverse('reviews:deactivated_reviews'))  # возвращает на страницу неактивных отзывов
    else:  # то же самое но обратно
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:list_reviews'))
