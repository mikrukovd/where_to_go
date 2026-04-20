from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from places.models import Place


def show_index(request):
    places = Place.objects.all()

    places_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f'/places/{place.id}/'
            }
        }
        places_geojson["features"].append(feature)

    return render(request, 'index.html', context={'places_geojson': places_geojson})


def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    response = {
        "title": place.title,
        "imgs": [img.image.url for img in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat
        }
    }

    # json_dumps_params={'ensure_ascii': False} для русских букв
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
