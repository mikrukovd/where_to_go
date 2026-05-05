from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from places import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_index),
    path('places/<int:place_id>/', views.place_detail, name='place_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [*urlpatterns,] + debug_toolbar_urls()
