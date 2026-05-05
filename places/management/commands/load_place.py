import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Загрузка данных о месте из JSON по URL'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL JSON с данными')

    def handle(self, *args, **options):
        url = options['url']

        try:
            response = requests.get(url)
            response.raise_for_status()
            place_raw = response.json()
        except requests.exceptions.RequestException as e:
            raise CommandError(f'Ошибка загрузки данных: {e}')
        except ValueError as e:
            raise CommandError(f'Ошибка парсинга JSON: {e}')

        place_details = [place_raw]
        for place_detail in place_details:
            title = place_detail['title']
            lng = float(place_detail['coordinates']['lng'])
            lat = float(place_detail['coordinates']['lat'])
            short_description = place_detail['description_short']
            long_description = place_detail['description_long']
            imgs = place_detail['imgs']

            place, created = Place.objects.get_or_create(
                title=title,
                defaults={
                    'lng': lng,
                    'lat': lat,
                    'short_description': short_description,
                    'long_description': long_description,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Создано место: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Место уже существует, обновляем: {title}'))
                place.lng = lng
                place.lat = lat
                place.short_description = short_description
                place.long_description = long_description
                place.save()
                place.images.all().delete()

            for idx, image_url in enumerate(imgs):
                if not image_url:
                    continue
                try:
                    img_response = requests.get(image_url)
                    img_response.raise_for_status()
                    image_name = image_url.split('/')[-1]
                    if not image_name or '.' not in image_name:
                        image_name = f'image_{idx}.jpg'
                    image_file = ContentFile(img_response.content, name=image_name)
                    PlaceImage.objects.create(place=place, image=image_file, order=idx)
                    self.stdout.write(self.style.SUCCESS(f'Добавлено изображение: {image_name}'))
                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f'Ошибка загрузки изображения {image_url}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'\nЗагружено/обновлено мест: {title}'))
