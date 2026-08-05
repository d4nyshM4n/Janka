from django.db import models
from menu.models import Dish


class Order(models.Model):

    STATUS = [
        ("new", "Новый"),
        ("cook", "Готовится"),
        ("ready", "Готов"),
        ("done", "Выдан"),
        ("cancel", "Отменен"),
    ]

    PAYMENT = [
        ("cash", "Наличные"),
        ("card", "Карта"),
    ]

    fullname = models.CharField(max_length=150)

    phone = models.CharField(max_length=30)

    address = models.CharField(max_length=255)

    pickup = models.BooleanField(default=False)

    dishes = models.ManyToManyField(Dish)

    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    payment = models.CharField(
        max_length=20,
        choices=PAYMENT
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="new"
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"