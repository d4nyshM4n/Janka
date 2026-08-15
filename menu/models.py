from django.db import models
from django.utils.text import slugify


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        null=True,
        blank=True,
        verbose_name="URL Slug"
    )

    order = models.IntegerField(
        default=0,
        verbose_name="Порядок"
    )

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["order"]


class Dish(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Название"
    )

    slug = models.SlugField(
        max_length=160,
        unique=True,
        null=True,
        blank=True,
        verbose_name="URL Slug"
    )

    image = models.ImageField(
        upload_to="dishes/",
        verbose_name="Фото",
        null=True,
    )

    description = models.TextField(
        verbose_name="Описание"
    )

    ingredients = models.TextField(
        verbose_name="Состав",
        null=True,
    )

    weight = models.CharField(
        max_length=50,
        verbose_name="Вес",
        null=True,
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Цена"
    )

    breakfast = models.BooleanField(
        default=False,
        verbose_name="Завтрак"
    )

    soup = models.BooleanField(
        default=False,
        verbose_name="Супы"
    )
    main = models.BooleanField(
            default=False,
            verbose_name="Основные блюда"
        )
    salats = models.BooleanField(
            default=False,
            verbose_name="Салаты"
        )
    deserts = models.BooleanField(
            default=False,
            verbose_name="Десерты"
        )
    drinks = models.BooleanField(
            default=False,
            verbose_name="Напитки"
        )

    available = models.BooleanField(
        default=True,
        verbose_name="В наличии"
    )

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Dish.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"