from django.db import models


# Create your models here.
class Places(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        blank=True, null=True
    )
    description_short = models.TextField(
        verbose_name='Краткое описание',
        blank=True, null=True
    )
    description_long = models.TextField(
        verbose_name='Полное описание',
        blank=True, null=True
    )
    lng = models.FloatField(
        verbose_name='Долгота',
        blank=True, null=True
    )
    lat = models.FloatField(
        verbose_name='Широта',
        blank=True, null=True
    )
