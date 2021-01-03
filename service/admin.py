from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Category, Product, Services, Review, Rating, RatingStar


class ImageInlines(admin.TabularInline):
    model = Services
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)
    fields = ("name",)
    inlines = [ImageInlines, ]


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("author", "category", "price", "url", "status")
    list_filter = ("status",)
    search_fields = ("description", "category__name",)
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("status",)
    fieldsets = (
        (None, {
            "fields": ("author",)
        }),
        (None, {
            "fields": ("description", ("price", "poster", "get_image"),)
        }),
        (None, {
            "fields": ("category", "status",)
        }),
    )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "title")
    list_display_links = ("title",)
    fields = ("title",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "product", "ip")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ("name", "email", "parent", "product", "id")
    readonly_fields = ("name", "email")


admin.site.register(RatingStar)