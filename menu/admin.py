from django.contrib import admin
from .models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "order",
    )

    # Автоматически заполняет slug на основе name при вводе в админке
    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "order",
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "slug",
        "available",
    )

    list_filter = (
        "category",
        "available",
    )

    search_fields = (
        "name",
    )

    # Автоматически заполняет slug на основе name
    prepopulated_fields = {
    "slug": ("name",)  # Ключом ДОЛЖНО быть поле slug
}