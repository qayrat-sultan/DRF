from django.urls import path

from . import views


urlpatterns = [
    path("product/", views.ProductListView.as_view()),
    path("product/<int:pk>/", views.ProductDetailView.as_view()),
    path("review/", views.ReviewCreateView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
]

