from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1


class PlacesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [PlaceImageInline]


admin.site.register(Place, PlacesAdmin)
admin.site.register(PlaceImage)
