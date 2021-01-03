from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from rest_framework import generics, permissions

from .models import Product
from .serializers import ProductListSerializer, ReviewCreateSerializer, ProductDetailSerializer, CreateRatingSerializer
from .service import get_client_ip, ProductFilter


class ProductListView(generics.ListAPIView):
    """Вывод списка продуктов"""
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        products = Product.objects.filter(status=0).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return products


class ProductDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    queryset = Product.objects.filter(status=0)
    serializer_class = ProductDetailSerializer


class ReviewCreateView(APIView):
    """Добавление отзыва к фильму"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
