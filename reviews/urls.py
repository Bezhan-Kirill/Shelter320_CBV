from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import CategoryListView, UnactiveDogReviewListView


app_name = ReviewsConfig.name

urlpatterns = [
    path('<int:pk>/reviews/', CategoryListView.as_view(), name='review'),
    # path('<int:pk/reviews/>', DogReviewListView, name='reviews_list'),
    path('<int:pk>/deactivated/', UnactiveDogReviewListView.as_view(), name='review'),
]