from django.db import models


class Promotion(models.Model):

    title = models.CharField(
        max_length=150
    )

    image = models.ImageField(
        upload_to="promotions/"
    )

    description = models.TextField()

    end_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"