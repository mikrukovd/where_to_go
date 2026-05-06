from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        html_template = (
            '''<img src="{}" style="max-width: 200px; max-height: 200px;
            display:block; margin: auto;" />'''
        )

        return format_html(html_template, obj.image.url)

    image_preview.short_description = 'Предпросмотр'

    fields = ['image', 'image_preview']


@admin.register(Place)
class PlacesAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title',)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'order', 'image_preview')
    list_filter = ('place',)
    search_fields = ('place__title',)
    raw_id_fields = ('place',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return format_html(
            '<img src="{}" style="max-height: 100px;" />',
            obj.image.url
        )

    image_preview.short_description = 'Предпросмотр'