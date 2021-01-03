from django.contrib.auth.models import User
from django.db import models
import transliterate
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """Категория"""
    name = models.CharField("Услуга", max_length=64)
    url = models.SlugField(max_length=70, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, **kwargs):
        super(Category, self).save()
        if not self.url:
            self.url = slugify(transliterate.translit(self.name, "ru", reversed=True))
            super(Category, self).save()


class Services(models.Model):
    """Услуги"""
    category = models.ForeignKey(Category, verbose_name="Услуга", blank=True, null=True, on_delete=models.CASCADE, default=None)
    title = models.CharField("Наименование", max_length=100)
    url = models.SlugField(max_length=70, unique=True, blank=True, null=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.title = None

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга категории"
        verbose_name_plural = "Услуги категории"

    def save(self, **kwargs):
        super(Services, self).save()
        if not self.url:
            self.url = slugify(transliterate.translit(self.title, "ru", reversed=True))
            super(Services, self).save()


class Product(models.Model):
    """Продукт"""
    description = models.TextField("Описание")
    poster = models.ImageField("Главное фото", upload_to="product_images/", default="default.jpeg", blank=True,
                               null=True)
    price = models.PositiveIntegerField("Стоимость", default=0, help_text="Указывать в сумах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=70, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.SmallIntegerField("Статус", default=1) #0-не активный, 1-в модерации, 2-активный
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.url})

    def save(self, **kwargs):
        super(Product, self).save()
        if not self.url:
            self.url = slugify(self.description) + '-' + str(self.id)
            super(Product, self).save()


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


