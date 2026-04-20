from django.db import models
from tinymce import models as tinymce_models


class Place(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    description_short = models.TextField(
        verbose_name='Краткое описание',
    )
    description_long = tinymce_models.HTMLField(
        verbose_name='Полное описание',
    )
    lng = models.FloatField(
        verbose_name='Долгота',
        default=0.0
    )
    lat = models.FloatField(
        verbose_name='Широта',
        default=0.0
    )

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField(
        verbose_name='Картинка'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Позиция'
    )

    class Meta:
        ordering = ['order']

        indexes = [
            models.Index(fields=['order'])
        ]

    def __str__(self):
        return f'{self.order} - {self.place.title}'
