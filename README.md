# Афиша

Веб-приложение на Django для просмотра достопримечательностей Москвы на интерактивной карте.

## Описание

Проект представляет собой карту с отмеченными местами для посещения. При клике на маркер открывается боковая панель с подробной информацией о месте: название, краткое и полное описание, фотографии.

## Технологии

- **Backend:** Django 5.2
- **База данных:** SQLite3
- **Frontend:** Vue.js 2.6, Leaflet (карты), Bootstrap 4.5
- **Дополнительно:**
  - django-admin-sortable2 — сортировка изображений в админке
  - django-tinymce — WYSIWYG-редактор для описаний
  - environs — управление переменными окружения
  - Pillow — работа с изображениями

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd where_to_go
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корне проекта:
   ```env
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Примените миграции:
   ```bash
   python manage.py migrate
   ```

6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

7. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

8. Откройте в браузере: `http://127.0.0.1:8000/`

## Админ-панель

Доступна по адресу: `http://127.0.0.1:8000/admin/`

В админке можно:
- Добавлять, редактировать и удалять места (Place)
- Загружать фотографии для каждого места
- Менять порядок отображения фотографий (drag-and-drop)
- Использовать визуальный редактор для полного описания

## Структура проекта

```
where_to_go/
├── manage.py
├── requirements.txt
├── places/                 # Приложение с моделями мест
│   ├── models.py           # Place, PlaceImage
│   ├── admin.py            # Настройка админки
│   └── views.py
├── where_to_go/            # Основной проект Django
│   ├── settings.py
│   ├── urls.py
│   └── views.py            # show_index, place_detail
├── templates/
│   └── index.html          # Главная страница с картой
├── media/                  # Загруженные изображения
└── static/
    └── where_to_go/        # Статические файлы (CSS, JS, иконки)
```

## Модели данных

### Place
- `title` — название места
- `description_short` — краткое описание
- `description_long` — полное описание (HTML)
- `lng` — долгота
- `lat` — широта

### PlaceImage
- `place` — связь с местом
- `image` — файл изображения
- `order` — порядок отображения

## Команда загрузки данных

### `load_place` — загрузка мест из JSON по URL

Команда скачивает JSON-файл с указанным URL и создаёт (или обновляет) места в базе данных, включая загрузку изображений.

```bash
python manage.py load_place <URL>
```

**Пример:**
```bash
python manage.py load_place https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/Антикафе%20Bizone.json
```

Команда:
- Создаёт новые места или обновляет существующие (по `title`)
- Скачивает изображения по URL из поля `images` и сохраняет в `ImageField`
- Поддерживает поля: `title`, `lng`/`longitude`, `lat`/`latitude`, `description_short`, `description_long`

## API

- `GET /` — главная страница с картой
- `GET /places/<place_id>/` — JSON с информацией о месте

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django |
| `DJANGO_DEBUG` | Режим отладки (True/False) |
| `ALLOWED_HOSTS` | Список разрешённых хостов |
