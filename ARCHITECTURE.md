# Архитектура проекта DRF LMS

## Общая структура

```
drf_homework/
│
├── config/                      # Основная конфигурация проекта
│   ├── __init__.py
│   ├── settings.py             # Настройки Django
│   ├── urls.py                 # Главный маршрутизатор URL
│   ├── wsgi.py                 # WSGI конфигурация
│   └── asgi.py                 # ASGI конфигурация
│
├── users/                       # Приложение пользователей
│   ├── __init__.py
│   ├── models.py               # Модель User
│   ├── admin.py                # Админ-панель для User
│   ├── apps.py                 # Конфигурация приложения
│   ├── serializers.py          # DRF сериализаторы
│   ├── views.py                # ViewSet для User
│   ├── urls.py                 # URL маршруты для users
│   └── migrations/             # Миграции базы данных
│
├── lms/                         # Приложение LMS (курсы и уроки)
│   ├── __init__.py
│   ├── models.py               # Модели Course и Lesson
│   ├── admin.py                # Админ-панель для LMS
│   ├── apps.py                 # Конфигурация приложения
│   ├── serializers.py          # DRF сериализаторы
│   ├── views.py                # Views (ViewSet и Generic)
│   ├── urls.py                 # URL маршруты для lms
│   └── migrations/             # Миграции базы данных
│
├── media/                       # Медиа файлы (загруженные изображения)
│   ├── courses/
│   │   └── previews/
│   ├── lessons/
│   │   └── previews/
│   └── users/
│       └── avatars/
│
├── manage.py                    # Django management скрипт
├── requirements.txt             # Зависимости проекта
├── .gitignore                  # Git ignore файл
├── README.md                   # Основная документация
├── INSTALLATION.md             # Инструкции по установке
├── API_EXAMPLES.md             # Примеры API запросов
└── DRF_LMS_Postman_Collection.json  # Postman коллекция
```

## Описание компонентов

### 1. Config (Главная конфигурация)

**settings.py** - содержит все настройки Django:
- `INSTALLED_APPS`: список установленных приложений
- `REST_FRAMEWORK`: настройки DRF
- `AUTH_USER_MODEL`: указание на кастомную модель User
- `MEDIA_ROOT` и `MEDIA_URL`: настройки для медиа-файлов
- Настройки базы данных (SQLite по умолчанию)

**urls.py** - главный маршрутизатор:
```python
/admin/              -> Django Admin
/api/users/          -> Users app URLs
/api/                -> LMS app URLs
```

### 2. Users App (Приложение пользователей)

#### Модель User
```python
class User(AbstractUser):
    email       # Email для авторизации (unique)
    phone       # Телефон
    city        # Город
    avatar      # Аватар (ImageField)
```

**Особенности:**
- Наследуется от `AbstractUser`
- Убрано поле `username`
- `USERNAME_FIELD = 'email'` - авторизация по email

#### API Endpoints (через ViewSet)
```
GET     /api/users/         - Список пользователей
POST    /api/users/         - Создать пользователя
GET     /api/users/{id}/    - Получить пользователя
PUT     /api/users/{id}/    - Обновить пользователя
PATCH   /api/users/{id}/    - Частично обновить
DELETE  /api/users/{id}/    - Удалить пользователя
```

### 3. LMS App (Система управления обучением)

#### Модель Course
```python
class Course(models.Model):
    title           # Название
    preview         # Превью (ImageField)
    description     # Описание
```

#### Модель Lesson
```python
class Lesson(models.Model):
    title           # Название
    description     # Описание
    preview         # Превью (ImageField)
    video_url       # Ссылка на видео
    course          # ForeignKey -> Course
```

**Связь между моделями:**
- Один курс может содержать много уроков (One-to-Many)
- Связь через `ForeignKey` с `related_name='lessons'`
- При удалении курса удаляются все его уроки (`on_delete=models.CASCADE`)

#### API Endpoints

**Курсы (через ViewSet):**
```
GET     /api/courses/         - Список курсов
POST    /api/courses/         - Создать курс
GET     /api/courses/{id}/    - Получить курс
PUT     /api/courses/{id}/    - Обновить курс
PATCH   /api/courses/{id}/    - Частично обновить
DELETE  /api/courses/{id}/    - Удалить курс
```

**Уроки (через Generic-классы):**
```
GET     /api/lessons/                - Список уроков
POST    /api/lessons/                - Создать урок
GET     /api/lessons/{id}/           - Получить урок
PUT     /api/lessons/{id}/update/    - Обновить урок
PATCH   /api/lessons/{id}/update/    - Частично обновить
DELETE  /api/lessons/{id}/delete/    - Удалить урок
```

## Паттерны проектирования

### 1. ViewSet vs Generic Views

**ViewSet (для Courses и Users):**
- Автоматически создает все CRUD endpoints
- Использует роутеры для генерации URL
- Меньше кода, больше автоматизации
- Подходит для стандартных CRUD операций

```python
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
```

**Generic Views (для Lessons):**
- Отдельный класс для каждой операции
- Больше контроля над каждым endpoint
- Гибкость в настройке URL
- Явное определение поведения

```python
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
```

### 2. Serializers

**Базовые сериализаторы:**
- `UserSerializer` - для модели User
- `CourseSerializer` - для модели Course (с вложенными уроками)
- `LessonSerializer` - для модели Lesson

**Особенности CourseSerializer:**
```python
class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
```
- Вычисляемое поле `lessons_count`
- Вложенная сериализация уроков
- Read-only для вложенных данных

### 3. Admin Panel

**Инлайны:**
- `LessonInline` в `CourseAdmin` - для редактирования уроков прямо в курсе

**Кастомизация:**
- `list_display` - отображаемые поля в списке
- `search_fields` - поля для поиска
- `list_filter` - фильтры

## Поток данных

### 1. Создание курса с уроками

```
1. POST /api/courses/
   {
     "title": "Python курс",
     "description": "Описание"
   }
   -> Создается Course с id=1

2. POST /api/lessons/
   {
     "title": "Урок 1",
     "course": 1
   }
   -> Создается Lesson, связанный с Course

3. GET /api/courses/1/
   -> Возвращается Course с вложенными lessons
```

### 2. Загрузка изображений

```
1. Client отправляет multipart/form-data
2. Django обрабатывает файл
3. Файл сохраняется в MEDIA_ROOT
4. В БД сохраняется путь к файлу
5. Файл доступен через MEDIA_URL
```

## База данных

### Схема SQLite

```
users_user
├── id (PK)
├── email (unique)
├── first_name
├── last_name
├── phone
├── city
├── avatar
├── password
├── is_staff
├── is_active
└── date_joined

lms_course
├── id (PK)
├── title
├── preview
└── description

lms_lesson
├── id (PK)
├── title
├── description
├── preview
├── video_url
└── course_id (FK -> lms_course.id)
```

### Связи

```
Course (1) ----< (Many) Lesson
    |
    └─ related_name='lessons'
```

## REST API Спецификация

### HTTP методы

| Метод  | Назначение           | Идемпотентность |
|--------|---------------------|-----------------|
| GET    | Получение данных    | Да              |
| POST   | Создание данных     | Нет             |
| PUT    | Полное обновление   | Да              |
| PATCH  | Частичное обновление| Нет             |
| DELETE | Удаление            | Да              |

### Коды ответов

| Код | Значение                    |
|-----|-----------------------------|
| 200 | OK - успешный запрос        |
| 201 | Created - создан объект     |
| 204 | No Content - удален объект  |
| 400 | Bad Request - ошибка данных |
| 404 | Not Found - не найдено      |
| 500 | Server Error - ошибка сервера|

### Формат ответов

**Список объектов:**
```json
[
  {
    "id": 1,
    "title": "Course 1",
    ...
  },
  {
    "id": 2,
    "title": "Course 2",
    ...
  }
]
```

**Один объект:**
```json
{
  "id": 1,
  "title": "Course 1",
  ...
}
```

**Ошибка валидации:**
```json
{
  "field_name": [
    "Это поле обязательно."
  ]
}
```

## Безопасность

**Текущее состояние (по заданию):**
- ❌ Авторизация не настроена
- ❌ Аутентификация не требуется
- ❌ Права доступа не проверяются
- ✅ CSRF защита включена (по умолчанию)

**Для продакшена потребуется:**
- Добавить авторизацию (JWT, Session, etc.)
- Настроить права доступа (Permissions)
- Добавить валидацию данных
- Настроить CORS
- Использовать HTTPS
- Изменить SECRET_KEY
- DEBUG = False

## Масштабирование

**Возможные улучшения:**
1. Добавить пагинацию для больших списков
2. Добавить фильтрацию и сортировку
3. Добавить поиск по текстовым полям
4. Кэширование популярных запросов
5. Оптимизация запросов (select_related, prefetch_related)
6. Версионирование API
7. Документация через Swagger/OpenAPI
8. Юнит-тесты и интеграционные тесты

## Примечания

- Проект использует SQLite (не для продакшена!)
- Медиа-файлы хранятся локально
- DEBUG режим включен
- Нет ограничений по размеру загружаемых файлов
- Нет валидации URL видео
- 