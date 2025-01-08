from django.urls import path

from reviews.apps import ReviewsConfig

from reviews.views import ReviewListView, ReviewDeactivatedListView, ReviewCreateView, ReviewDetailView, \
    ReviewUpdateView, ReviewDeleteView, review_toggle_activity

app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListView.as_view(), name='list_reviews'),
    path('deactivated/', ReviewDeactivatedListView.as_view(), name='deactivated_reviews'),
    path('review/create/', ReviewCreateView.as_view(), name='create_reviews'),
    path('review/detail/<slug:slug>/', ReviewDetailView.as_view(), name='detail_review'),
    path('review/update/<slug:slug>/', ReviewUpdateView.as_view(), name='update_review'),
    path('review/delete/<slug:slug>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('review/toggle/<slug:slug>/', review_toggle_activity, name='toggle_activity_review'),
]