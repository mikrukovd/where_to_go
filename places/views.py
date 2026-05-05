from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def show_index(request):
    places = Place.objects.all()

    features = [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lng, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': reverse('place_detail', args=[place.id])
            }
        }
        for place in places
    ]

    places_geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    return render(request, 'index.html', context={'places_geojson': places_geojson})


def place_detail(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related('images'), id=place_id)

    response = {
        'title': place.title,
        'imgs': [img.image.url for img in place.images.all()],
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat
        }
    }

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
