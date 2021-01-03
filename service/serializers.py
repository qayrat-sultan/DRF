from rest_framework import serializers

from .models import Product, Review, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ProductListSerializer(serializers.ModelSerializer):
    """Spisok uslug"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ("id", "poster", "description", "category", "rating_user", "middle_star", "price")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыво"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class ProductDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    # category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    # price = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    author = serializers.CharField(source="author.username")
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        exclude = ("created", "updated")


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "product")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            product=validated_data.get('product', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating