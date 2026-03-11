from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="200" height="200" />')

    image_preview.short_description = 'Предпросмотр'

    fields = ['image', 'image_preview', 'order']


class PlacesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [PlaceImageInline]


admin.site.register(Place, PlacesAdmin)
admin.site.register(PlaceImage)
