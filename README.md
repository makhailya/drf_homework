# Django REST Framework - LMS проект

Проект системы управления обучением (Learning Management System) с использованием Django и Django REST Framework.

## Описание

Проект содержит:
- Кастомную модель пользователя с авторизацией по email
- Модели курсов и уроков
- REST API для всех моделей
- CRUD операции для курсов (через ViewSet) и уроков (через Generic-классы)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <your-repository-url>
cd drf_homework
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

При создании вас попросят ввести email и пароль (без username).

### 6. Запуск сервера

```bash
python manage.py runserver
```

Проект будет доступен по адресу: http://127.0.0.1:8000/

## Структура проекта

```
drf_homework/
├── config/              # Основная конфигурация проекта
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/               # Приложение пользователей
│   ├── models.py       # Кастомная модель User
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── lms/                 # Приложение курсов и уроков
│   ├── models.py       # Модели Course и Lesson
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── media/               # Медиа-файлы
├── manage.py
├── requirements.txt
└── .gitignore
```

## Модели

### User (users/models.py)
- **email** - Email (используется для авторизации)
- **phone** - Телефон
- **city** - Город
- **avatar** - Аватар

### Course (lms/models.py)
- **title** - Название курса
- **preview** - Превью (картинка)
- **description** - Описание курса

### Lesson (lms/models.py)
- **title** - Название урока
- **description** - Описание урока
- **preview** - Превью (картинка)
- **video_url** - Ссылка на видео
- **course** - Связь с курсом (ForeignKey)

## API Endpoints

### Пользователи (Users)

**Базовый URL:** `/api/users/`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/users/` | Список всех пользователей |
| POST | `/api/users/` | Создать пользователя |
| GET | `/api/users/{id}/` | Получить пользователя по ID |
| PUT | `/api/users/{id}/` | Обновить пользователя |
| PATCH | `/api/users/{id}/` | Частично обновить пользователя |
| DELETE | `/api/users/{id}/` | Удалить пользователя |

### Курсы (Courses) - ViewSet

**Базовый URL:** `/api/courses/`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/courses/` | Список всех курсов |
| POST | `/api/courses/` | Создать курс |
| GET | `/api/courses/{id}/` | Получить курс по ID |
| PUT | `/api/courses/{id}/` | Обновить курс |
| PATCH | `/api/courses/{id}/` | Частично обновить курс |
| DELETE | `/api/courses/{id}/` | Удалить курс |

### Уроки (Lessons) - Generic Views

**Базовый URL:** `/api/lessons/`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/lessons/` | Список всех уроков |
| POST | `/api/lessons/` | Создать урок |
| GET | `/api/lessons/{id}/` | Получить урок по ID |
| PUT/PATCH | `/api/lessons/{id}/update/` | Обновить урок |
| DELETE | `/api/lessons/{id}/delete/` | Удалить урок |

## Примеры запросов в Postman

### 1. Создание курса (POST)

**URL:** `http://127.0.0.1:8000/api/courses/`

**Method:** POST

**Body (raw JSON):**
```json
{
    "title": "Python для начинающих",
    "description": "Курс по основам программирования на Python"
}
```

### 2. Получение списка курсов (GET)

**URL:** `http://127.0.0.1:8000/api/courses/`

**Method:** GET

### 3. Создание урока (POST)

**URL:** `http://127.0.0.1:8000/api/lessons/`

**Method:** POST

**Body (raw JSON):**
```json
{
    "title": "Введение в Python",
    "description": "Первый урок курса",
    "video_url": "https://www.youtube.com/watch?v=example",
    "course": 1
}
```

### 4. Получение урока по ID (GET)

**URL:** `http://127.0.0.1:8000/api/lessons/1/`

**Method:** GET

### 5. Обновление урока (PUT)

**URL:** `http://127.0.0.1:8000/api/lessons/1/update/`

**Method:** PUT или PATCH

**Body (raw JSON):**
```json
{
    "title": "Введение в Python - обновлено",
    "description": "Обновленное описание первого урока",
    "video_url": "https://www.youtube.com/watch?v=new-example",
    "course": 1
}
```

### 6. Удаление урока (DELETE)

**URL:** `http://127.0.0.1:8000/api/lessons/1/delete/`

**Method:** DELETE

### 7. Создание пользователя (POST)

**URL:** `http://127.0.0.1:8000/api/users/`

**Method:** POST

**Body (raw JSON):**
```json
{
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "phone": "+371 12345678",
    "city": "Рига"
}
```

## Настройки Postman

1. Откройте Postman
2. Создайте новую коллекцию "DRF LMS"
3. Для каждого endpoint создайте новый запрос
4. В Headers добавьте:
   - `Content-Type: application/json` (для POST, PUT, PATCH)
5. Для загрузки изображений используйте `form-data` вместо `raw JSON`

## Тестирование через браузер

Django REST Framework предоставляет веб-интерфейс для тестирования API:

- Откройте http://127.0.0.1:8000/api/courses/ в браузере
- Откройте http://127.0.0.1:8000/api/lessons/ в браузере

## Админ-панель

Для доступа к админ-панели:

1. Перейдите по адресу: http://127.0.0.1:8000/admin/
2. Войдите используя email и пароль суперпользователя

## Особенности реализации

1. **Курсы (Course):**
   - Реализованы через ViewSet
   - Автоматически создаются все CRUD endpoints
   - При получении курса возвращается список связанных уроков

2. **Уроки (Lesson):**
   - Реализованы через Generic-классы
   - Каждая операция имеет отдельный класс и endpoint
   - Связаны с курсом через ForeignKey

3. **Пользователи (User):**
   - Кастомная модель с авторизацией по email
   - Убрано поле username
   - Добавлены поля: phone, city, avatar

## Зависимости

- Django 5.0.1
- djangorestframework 3.14.0
- Pillow 10.2.0 (для работы с изображениями)

## Примечания

- База данных: SQLite (по умолчанию)
- Медиа-файлы сохраняются в папке `media/`
- DEBUG режим включен (для продакшена отключите в settings.py)
- Авторизация и права доступа не настроены (по заданию)

## Автор

Ваше имя

## Лицензия

MIT