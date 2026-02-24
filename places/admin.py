from django.contrib import admin
from .models import Places
# Register your models here.


class PlacesAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Places, PlacesAdmin)
