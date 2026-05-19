# Инструкция по запуску проекта

## Быстрый старт

### 1. Подготовка окружения

```bash
# Клонирование репозитория
git clone <your-repo-url>
cd drf_homework

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
# Для Linux/Mac:
source venv/bin/activate
# Для Windows:
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate
```

### 3. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Вам будет предложено ввести:
- Email: admin@example.com
- Password: (ваш пароль)
- Password (again): (повторите пароль)

**Примечание:** Username не запрашивается, так как авторизация происходит по email.

### 4. Запуск сервера

```bash
python manage.py runserver
```

Сервер запустится по адресу: http://127.0.0.1:8000/

## Проверка работы

### 1. Админ-панель

Откройте http://127.0.0.1:8000/admin/ и войдите с помощью созданного суперпользователя.

### 2. API Endpoints

- Курсы: http://127.0.0.1:8000/api/courses/
- Уроки: http://127.0.0.1:8000/api/lessons/
- Пользователи: http://127.0.0.1:8000/api/users/

### 3. Browsable API

DRF предоставляет веб-интерфейс для тестирования API. Просто откройте любой endpoint в браузере.

## Заполнение тестовыми данными

### Через админ-панель

1. Перейдите в админ-панель
2. Создайте несколько курсов
3. Для каждого курса создайте несколько уроков

### Через API (Postman)

Используйте примеры из файла `API_EXAMPLES.md`

### Через Django shell

```bash
python manage.py shell
```

```python
from lms.models import Course, Lesson

# Создание курса
course = Course.objects.create(
    title="Python для начинающих",
    description="Полный курс по основам Python"
)

# Создание уроков
Lesson.objects.create(
    title="Введение в Python",
    description="Первый урок курса",
    video_url="https://www.youtube.com/watch?v=intro",
    course=course
)

Lesson.objects.create(
    title="Переменные и типы данных",
    description="Второй урок курса",
    video_url="https://www.youtube.com/watch?v=variables",
    course=course
)

print(f"Создан курс: {course.title}")
print(f"Количество уроков: {course.lessons.count()}")
```

## Структура URL

```
/admin/                          - Админ-панель Django
/api/users/                      - CRUD для пользователей
/api/courses/                    - CRUD для курсов
/api/lessons/                    - Список и создание уроков
/api/lessons/{id}/               - Просмотр урока
/api/lessons/{id}/update/        - Обновление урока
/api/lessons/{id}/delete/        - Удаление урока
```

## Работа с изображениями

### Загрузка изображений через API

При отправке запросов с изображениями используйте `multipart/form-data`:

**В Postman:**
1. Выберите метод POST
2. Перейдите на вкладку "Body"
3. Выберите "form-data"
4. Добавьте текстовые поля и файлы

**Пример для курса:**
- `title` (Text): "Мой курс"
- `description` (Text): "Описание курса"
- `preview` (File): [выберите изображение]

### Доступ к загруженным изображениям

После загрузки изображения будут доступны по адресу:
- http://127.0.0.1:8000/media/courses/previews/filename.jpg
- http://127.0.0.1:8000/media/lessons/previews/filename.jpg
- http://127.0.0.1:8000/media/users/avatars/filename.jpg

## Полезные команды Django

```bash
# Создание новых миграций после изменения моделей
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Откат миграций
python manage.py migrate app_name migration_name

# Просмотр SQL для миграций
python manage.py sqlmigrate app_name migration_number

# Интерактивная оболочка Django
python manage.py shell

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статических файлов (для продакшена)
python manage.py collectstatic

# Запуск тестов
python manage.py test

# Проверка проекта на ошибки
python manage.py check
```

## Отладка

### Включение детального вывода ошибок

В `config/settings.py` уже установлено:
```python
DEBUG = True
```

### Просмотр SQL-запросов

В Django shell:
```python
from django.db import connection
from lms.models import Course

# Выполните запрос
courses = Course.objects.all()

# Посмотрите SQL
print(connection.queries)
```

### Логирование

Добавьте в `config/settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

## Решение проблем

### Ошибка при миграциях

```bash
# Удалите файл базы данных
rm db.sqlite3

# Удалите файлы миграций (кроме __init__.py)
rm lms/migrations/0*.py
rm users/migrations/0*.py

# Создайте миграции заново
python manage.py makemigrations
python manage.py migrate
```

### Ошибка с Pillow

Если возникают проблемы с установкой Pillow:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev
pip install Pillow
```

**macOS:**
```bash
brew install libjpeg
pip install Pillow
```

**Windows:**
- Скачайте wheel файл с https://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
- Установите: `pip install Pillow‑xxx.whl`

### Port already in use

Если порт 8000 занят:
```bash
# Запустите на другом порту
python manage.py runserver 8080

# Или найдите и остановите процесс
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Следующие шаги

После успешного запуска проекта:

1. ✅ Протестируйте все endpoints в Postman
2. ✅ Создайте тестовые данные
3. ✅ Проверьте связь между курсами и уроками
4. ✅ Загрузите изображения
5. ✅ Изучите DRF Browsable API
6. ✅ Экспериментируйте с разными типами запросов

## Дополнительные ресурсы

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Postman Documentation](https://learning.postman.com/)
- [Git Documentation](https://git-scm.com/doc)
- 