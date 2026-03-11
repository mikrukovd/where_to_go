from django.contrib import admin
from .models import Places, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1


class PlacesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [PlaceImageInline]


admin.site.register(Places, PlacesAdmin)
admin.site.register(PlaceImage)
