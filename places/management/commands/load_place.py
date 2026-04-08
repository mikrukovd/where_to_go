import requests
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Загрузка данных о местах из JSON по URL'

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            help='URL для загрузки JSON файла с данными'
        )

    def handle(self, *args, **options):
        url = options['url']

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise CommandError(f'Ошибка загрузки данных: {e}')
        except ValueError as e:
            raise CommandError(f'Ошибка парсинга JSON: {e}')

        # Если данные приходятся в виде списка объектов
        if isinstance(data, dict):
            # Возможна обёртка типа {"places": [...]} или {"data": [...]}
            places_data = data.get('places', data.get('data', [data]))
        elif isinstance(data, list):
            places_data = data
        else:
            raise CommandError('Неверный формат данных')

        places_count = 0

        for place_data in places_data:
            title = place_data.get('title', '')
            lng = place_data.get('lng', place_data.get('longitude'))
            lat = place_data.get('lat', place_data.get('latitude'))
            description_short = place_data.get('description_short', place_data.get('description'))
            description_long = place_data.get('description_long', place_data.get('description_full'))

            # Создание объекта
            place, created = Place.objects.get_or_create(
                title=title,
                defaults={
                    'lng': lng,
                    'lat': lat,
                    'description_short': description_short,
                    'description_long': description_long,
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Создано место: {title}')
                )
                places_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Место уже существует: {title}')
                )

            if not created:
                place.lng = lng
                place.lat = lat
                place.description_short = description_short
                place.description_long = description_long
                place.save()

            images = place_data.get('images', place_data.get('image', []))
            if isinstance(images, str):
                images = [images]

            for idx, image_url in enumerate(images):
                if not image_url:
                    continue

                try:
                    img_response = requests.get(image_url)
                    img_response.raise_for_status()

                    # Картинка из url
                    image_name = image_url.split('/')[-1]
                    if not image_name or '.' not in image_name:
                        image_name = f'image_{idx}.jpg'

                    image_file = ContentFile(
                        img_response.content,
                        name=image_name
                    )

                    PlaceImage.objects.create(
                        place=place,
                        image=image_file,
                        order=idx
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f'  Добавлено изображение: {image_name}')
                    )
                except requests.exceptions.RequestException as e:
                    self.stdout.write(
                        self.style.ERROR(f'  Ошибка загрузки изображения {image_url}: {e}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nЗагружено новых мест: {places_count}'
            )
        )
