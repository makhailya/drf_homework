# LMS API - Learning Management System

Полнофункциональный REST API для системы управления обучением на Django REST Framework.

## 🚀 Технологии

- **Backend**: Django 5.2, Django REST Framework
- **База данных**: PostgreSQL
- **Авторизация**: JWT (Simple JWT)
- **Асинхронные задачи**: Celery + Redis
- **Платежи**: Stripe
- **Документация**: drf-yasg (Swagger/ReDoc)
- **Тесты**: Django TestCase (87% coverage)

## 📋 Функционал

### Пользователи и авторизация
- Регистрация и JWT авторизация
- Кастомная модель User (email вместо username)
- Профиль пользователя с историей платежей
- Система прав доступа (модераторы, владельцы объектов)

### Курсы и уроки
- CRUD операции для курсов и уроков
- Nested сериализация (уроки внутри курса)
- Фильтрация и пагинация
- Валидация YouTube URL для видео
- Отслеживание владельцев контента

### Подписки
- Подписка/отписка на обновления курсов
- Асинхронная email-рассылка при обновлении курса
- Защита от спама (уведомления не чаще раза в 4 часа)

### Платежи
- Интеграция со Stripe для приёма платежей
- Создание платёжных сессий
- Проверка статуса оплаты
- История платежей пользователя

### Фоновые задачи
- Асинхронная отправка email через Celery
- Периодическая блокировка неактивных пользователей (30 дней)
- Celery Beat для планирования задач

## 🛠 Установка и запуск

### Предварительные требования

- Python 3.10+
- PostgreSQL 14+
- Redis 6+

### Установка

1. **Клонируйте репозиторий:**
```bash
git clone <your-repo-url>
cd drf_homework
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте PostgreSQL:**
```bash
psql postgres
CREATE DATABASE drf_lms_db;
CREATE USER drf_lms_user WITH PASSWORD 'your_password';
ALTER ROLE drf_lms_user SET client_encoding TO 'utf8';
ALTER ROLE drf_lms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE drf_lms_user SET timezone TO 'Europe/Riga';
GRANT ALL PRIVILEGES ON DATABASE drf_lms_db TO drf_lms_user;
ALTER USER drf_lms_user CREATEDB;
\q
```

5. **Создайте файл `.env`:**
```
DB_NAME=drf_lms_db
DB_USER=drf_lms_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here

REDIS_HOST=localhost
REDIS_PORT=6379

STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@lms.local
```

6. **Примените миграции:**
```bash
python manage.py migrate
```

7. **Создайте суперпользователя:**
```bash
python manage.py createsuperuser
```

8. **Создайте группу модераторов:**
```bash
python manage.py shell
>>> from django.contrib.auth.models import Group
>>> Group.objects.create(name='moderators')
>>> exit()
```

### Запуск

Вам потребуется **4 терминала**:

**Терминал 1 - Django:**
```bash
python manage.py runserver
```

**Терминал 2 - Redis:**
```bash
redis-server
```

**Терминал 3 - Celery Worker:**
```bash
celery -A config worker -l info
```

**Терминал 4 - Celery Beat:**
```bash
celery -A config beat -l info
```

## 📖 API Документация

После запуска сервера документация доступна по адресам:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/swagger.json

## 🧪 Тестирование

Запуск тестов:
```bash
python manage.py test
```

Проверка покрытия:
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # HTML отчёт в htmlcov/index.html
```

Текущее покрытие: **87%**

## 🔑 Основные эндпоинты

### Авторизация
- `POST /api/token/` - Получить JWT токен
- `POST /api/token/refresh/` - Обновить токен
- `POST /api/users/` - Регистрация (без токена)

### Курсы
- `GET /api/courses/` - Список курсов
- `POST /api/courses/` - Создать курс
- `GET /api/courses/{id}/` - Детали курса
- `PATCH /api/courses/{id}/` - Обновить курс
- `DELETE /api/courses/{id}/` - Удалить курс

### Уроки
- `GET /api/lessons/` - Список уроков
- `POST /api/lessons/` - Создать урок
- `GET /api/lessons/{id}/` - Детали урока
- `PATCH /api/lessons/{id}/update/` - Обновить урок
- `DELETE /api/lessons/{id}/delete/` - Удалить урок

### Подписки
- `POST /api/subscription/` - Подписаться/отписаться от курса

### Платежи
- `GET /api/payments/` - Список платежей
- `POST /api/payments/` - Создать платёж (получить ссылку на оплату)
- `GET /api/payments/{id}/status/` - Проверить статус платежа

## 👥 Права доступа

### Обычные пользователи
- ✅ Создавать курсы и уроки
- ✅ Редактировать свои курсы и уроки
- ✅ Удалять свои курсы и уроки
- ✅ Просматривать только свой контент

### Модераторы
- ✅ Просматривать все курсы и уроки
- ✅ Редактировать любые курсы и уроки
- ❌ Создавать курсы и уроки
- ❌ Удалять курсы и уроки

## 💳 Тестовые карты Stripe

Для тестирования платежей используйте:
- **Успешная оплата**: 4242 4242 4242 4242
- **Требуется аутентификация**: 4000 0025 0000 3155
- **Отклонена**: 4000 0000 0000 9995

Дата: любая будущая, CVC: любой 3-значный код

## 📧 Email уведомления

В режиме разработки письма выводятся в консоль Django.

Для production настройте реальный SMTP в `.env`:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## 🔄 Celery задачи

### Асинхронные задачи
- **send_course_update_notification** - Рассылка при обновлении курса

### Периодические задачи (Celery Beat)
- **deactivate_inactive_users** - Блокировка пользователей без активности > 30 дней (запуск каждый день в 00:00)

## 📦 Структура проекта
```
drf_homework/
├── config/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── users/               # Приложение пользователей
│   ├── models.py        # User, Payment
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   └── tasks.py         # Celery задачи
├── lms/                 # Приложение обучения
│   ├── models.py        # Course, Lesson, Subscription
│   ├── views.py
│   ├── serializers.py
│   ├── validators.py
│   ├── paginators.py
│   └── tasks.py         # Celery задачи
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🐛 Известные ограничения

- Email отправка работает только в тестовом режиме (console backend)
- Stripe работает в тестовом режиме
- Celery Beat требует отдельного процесса

## 📄 Лицензия

Учебный проект

## 👨‍💻 Автор

Ваше имя - SkyPro Django курс
```

### Шаг 4: Обновите .gitignore

Убедитесь, что `.gitignore` содержит:
```
# Environment
.env
*.pyc
__pycache__/
*.py[cod]
*$py.class

# Database
*.sqlite3
db.sqlite3

# Media
media/

# Static
staticfiles/

# Coverage
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover

# Celery
celerybeat-schedule
celerybeat.pid

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

### Шаг 5: Создайте `.env.example`
```
# Database
DB_NAME=drf_lms_db
DB_USER=drf_lms_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Stripe
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@lms.local
