from django.db import models


class Reservation(models.Model):

    STATUS = [
        ("yes", "Подтверждено"),
        ("no", "Отменено"),
    ]

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=30
    )

    date = models.DateField()

    time = models.TimeField()

    guests = models.IntegerField()

    comment = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="yes"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"