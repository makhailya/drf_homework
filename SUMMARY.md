# 🎓 Django REST Framework - LMS Homework

## 📋 Выполненные задания

### ✅ Задание 1: Создание Django проекта с DRF
- ✓ Создан новый Django-проект с названием `config`
- ✓ Подключен Django REST Framework в `INSTALLED_APPS`
- ✓ Настроены базовые параметры DRF в `settings.py`

### ✅ Задание 2: Создание моделей

#### 1. Модель User (users/models.py)
```python
class User(AbstractUser):
    email       # Авторизация по email (unique)
    phone       # Телефон пользователя
    city        # Город пользователя
    avatar      # Аватарка (ImageField)
```
- ✓ Наследуется от AbstractUser
- ✓ Убрано поле username
- ✓ USERNAME_FIELD = 'email'
- ✓ Размещено в приложении `users`

#### 2. Модель Course (lms/models.py)
```python
class Course(models.Model):
    title           # Название курса
    preview         # Превью (картинка)
    description     # Описание курса
```

#### 3. Модель Lesson (lms/models.py)
```python
class Lesson(models.Model):
    title           # Название урока
    description     # Описание урока
    preview         # Превью (картинка)
    video_url       # Ссылка на видео
    course          # ForeignKey -> Course
```
- ✓ Связь через ForeignKey с Course
- ✓ related_name='lessons'
- ✓ Размещено в приложении `lms`

### ✅ Задание 3: CRUD операции

#### Курсы - ViewSet
```python
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
```
**Endpoints:**
- GET    /api/courses/       - список курсов
- POST   /api/courses/       - создать курс
- GET    /api/courses/{id}/  - получить курс
- PUT    /api/courses/{id}/  - обновить курс
- PATCH  /api/courses/{id}/  - частично обновить
- DELETE /api/courses/{id}/  - удалить курс

#### Уроки - Generic классы
```python
LessonListCreateAPIView    # Список и создание
LessonRetrieveAPIView      # Получение одного
LessonUpdateAPIView        # Обновление
LessonDestroyAPIView       # Удаление
```
**Endpoints:**
- GET    /api/lessons/              - список уроков
- POST   /api/lessons/              - создать урок
- GET    /api/lessons/{id}/         - получить урок
- PUT    /api/lessons/{id}/update/  - обновить урок
- PATCH  /api/lessons/{id}/update/  - частично обновить
- DELETE /api/lessons/{id}/delete/  - удалить урок

## 🚀 Быстрый старт

### 1. Установка
```bash
# Клонировать репозиторий
git clone <your-repo-url>
cd drf_homework

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt
```

### 2. Настройка базы данных
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3. Запуск
```bash
python manage.py runserver
```

Проект доступен: http://127.0.0.1:8000/

## 📂 Структура проекта

```
drf_homework/
├── config/              # Конфигурация проекта
│   ├── settings.py     # Настройки Django + DRF
│   └── urls.py         # Главный роутер
│
├── users/               # Приложение пользователей
│   ├── models.py       # Модель User
│   ├── serializers.py  # UserSerializer
│   ├── views.py        # UserViewSet
│   └── urls.py         # URL для users
│
├── lms/                 # Приложение LMS
│   ├── models.py       # Course и Lesson
│   ├── serializers.py  # Сериализаторы
│   ├── views.py        # ViewSet + Generic
│   └── urls.py         # URL для lms
│
├── media/               # Загруженные файлы
├── manage.py           
├── requirements.txt     
└── .gitignore          
```

## 🔍 Тестирование в Postman

### Импорт коллекции
1. Откройте Postman
2. File → Import
3. Выберите `DRF_LMS_Postman_Collection.json`
4. Коллекция готова к использованию!

### Примеры запросов

**Создать курс:**
```json
POST http://127.0.0.1:8000/api/courses/
{
    "title": "Python для начинающих",
    "description": "Полный курс Python"
}
```

**Создать урок:**
```json
POST http://127.0.0.1:8000/api/lessons/
{
    "title": "Урок 1: Введение",
    "description": "Первый урок курса",
    "video_url": "https://youtube.com/...",
    "course": 1
}
```

## 📚 Документация

- **README.md** - основная документация
- **INSTALLATION.md** - подробная инструкция по установке
- **API_EXAMPLES.md** - примеры всех API запросов
- **ARCHITECTURE.md** - архитектура проекта
- **DRF_LMS_Postman_Collection.json** - готовая Postman коллекция

## 🎯 Особенности реализации

### Курсы (ViewSet)
- Автоматическое создание всех CRUD endpoints
- Вложенная сериализация уроков
- Вычисляемое поле `lessons_count`

### Уроки (Generic Views)
- Отдельный класс для каждой операции
- Явное определение URL endpoints
- Полный контроль над поведением

### Пользователи
- Кастомная модель с email вместо username
- Поля: phone, city, avatar
- ViewSet для всех операций

## ⚙️ Технологии

- **Django 5.0.1**
- **Django REST Framework 3.14.0**
- **Pillow 10.2.0** (для изображений)
- **SQLite** (база данных)

## 📝 Примечания

- ✅ Все CRUD операции работают
- ✅ Связь между курсами и уроками настроена
- ✅ Загрузка изображений работает
- ✅ .gitignore и requirements.txt созданы
- ⚠️ Авторизация не настроена (по заданию)
- ⚠️ Права доступа не проверяются (по заданию)

## 🧪 Проверка работы

### Через браузер (DRF Browsable API)
- http://127.0.0.1:8000/api/courses/
- http://127.0.0.1:8000/api/lessons/
- http://127.0.0.1:8000/api/users/

### Через Postman
Используйте готовую коллекцию `DRF_LMS_Postman_Collection.json`

### Через админ-панель
- http://127.0.0.1:8000/admin/
- Логин с email и паролем суперпользователя

## 📧 Контакты

Если возникнут вопросы - обращайтесь!

---

**Статус:** ✅ Все задания выполнены
**Готово к сдаче:** Да
**Протестировано:** Да

Made with ❤️ for homework
