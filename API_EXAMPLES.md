# Примеры API запросов для тестирования

## Курсы (Courses)

### 1. Получить список всех курсов
```
GET http://127.0.0.1:8000/api/courses/
```

### 2. Создать новый курс
```
POST http://127.0.0.1:8000/api/courses/
Content-Type: application/json

{
    "title": "Python для начинающих",
    "description": "Полный курс по основам программирования на Python"
}
```

### 3. Получить курс по ID
```
GET http://127.0.0.1:8000/api/courses/1/
```

### 4. Обновить курс (полное обновление)
```
PUT http://127.0.0.1:8000/api/courses/1/
Content-Type: application/json

{
    "title": "Python для начинающих - ОБНОВЛЕНО",
    "description": "Обновленное описание курса"
}
```

### 5. Частично обновить курс
```
PATCH http://127.0.0.1:8000/api/courses/1/
Content-Type: application/json

{
    "description": "Только обновление описания"
}
```

### 6. Удалить курс
```
DELETE http://127.0.0.1:8000/api/courses/1/
```

---

## Уроки (Lessons)

### 1. Получить список всех уроков
```
GET http://127.0.0.1:8000/api/lessons/
```

### 2. Создать новый урок
```
POST http://127.0.0.1:8000/api/lessons/
Content-Type: application/json

{
    "title": "Урок 1: Введение в Python",
    "description": "В этом уроке вы познакомитесь с основами Python",
    "video_url": "https://www.youtube.com/watch?v=example123",
    "course": 1
}
```

### 3. Получить урок по ID
```
GET http://127.0.0.1:8000/api/lessons/1/
```

### 4. Обновить урок
```
PUT http://127.0.0.1:8000/api/lessons/1/update/
Content-Type: application/json

{
    "title": "Урок 1: Введение в Python (обновлено)",
    "description": "Обновленное описание урока",
    "video_url": "https://www.youtube.com/watch?v=new-example",
    "course": 1
}
```

### 5. Частично обновить урок
```
PATCH http://127.0.0.1:8000/api/lessons/1/update/
Content-Type: application/json

{
    "video_url": "https://www.youtube.com/watch?v=updated-link"
}
```

### 6. Удалить урок
```
DELETE http://127.0.0.1:8000/api/lessons/1/delete/
```

---

## Пользователи (Users)

### 1. Получить список всех пользователей
```
GET http://127.0.0.1:8000/api/users/
```

### 2. Создать нового пользователя
```
POST http://127.0.0.1:8000/api/users/
Content-Type: application/json

{
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "phone": "+371 12345678",
    "city": "Рига"
}
```

### 3. Получить пользователя по ID
```
GET http://127.0.0.1:8000/api/users/1/
```

### 4. Обновить пользователя
```
PUT http://127.0.0.1:8000/api/users/1/
Content-Type: application/json

{
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Петров",
    "phone": "+371 87654321",
    "city": "Даугавпилс"
}
```

### 5. Частично обновить пользователя
```
PATCH http://127.0.0.1:8000/api/users/1/
Content-Type: application/json

{
    "city": "Юрмала"
}
```

### 6. Удалить пользователя
```
DELETE http://127.0.0.1:8000/api/users/1/
```

---

## Примеры с изображениями

### Создать курс с изображением
```
POST http://127.0.0.1:8000/api/courses/
Content-Type: multipart/form-data

В Postman:
- Выберите "Body" -> "form-data"
- Добавьте поля:
  - title: "Django курс" (Text)
  - description: "Описание курса" (Text)
  - preview: [выберите файл изображения] (File)
```

### Создать урок с изображением
```
POST http://127.0.0.1:8000/api/lessons/
Content-Type: multipart/form-data

В Postman:
- Выберите "Body" -> "form-data"
- Добавьте поля:
  - title: "Первый урок" (Text)
  - description: "Описание урока" (Text)
  - video_url: "https://youtube.com/watch?v=123" (Text)
  - course: 1 (Text)
  - preview: [выберите файл изображения] (File)
```

---

## Тестовые данные

### Создание нескольких курсов:

#### Курс 1:
```json
{
    "title": "Python для начинающих",
    "description": "Изучите основы программирования на Python с нуля"
}
```

#### Курс 2:
```json
{
    "title": "Django REST Framework",
    "description": "Создание REST API с использованием Django и DRF"
}
```

#### Курс 3:
```json
{
    "title": "Frontend разработка",
    "description": "HTML, CSS, JavaScript для начинающих"
}
```

### Создание уроков для курса 1:

#### Урок 1:
```json
{
    "title": "Введение в Python",
    "description": "Что такое Python и зачем его изучать",
    "video_url": "https://www.youtube.com/watch?v=intro",
    "course": 1
}
```

#### Урок 2:
```json
{
    "title": "Переменные и типы данных",
    "description": "Изучаем переменные и основные типы данных в Python",
    "video_url": "https://www.youtube.com/watch?v=variables",
    "course": 1
}
```

#### Урок 3:
```json
{
    "title": "Условные конструкции",
    "description": "If, elif, else - управление потоком выполнения",
    "video_url": "https://www.youtube.com/watch?v=conditions",
    "course": 1
}
```

---

## Ожидаемые ответы API

### Успешное создание курса:
```json
{
    "id": 1,
    "title": "Python для начинающих",
    "preview": null,
    "description": "Изучите основы программирования на Python с нуля",
    "lessons_count": 0,
    "lessons": []
}
```

### Список курсов с уроками:
```json
[
    {
        "id": 1,
        "title": "Python для начинающих",
        "preview": null,
        "description": "Изучите основы программирования на Python с нуля",
        "lessons_count": 3,
        "lessons": [
            {
                "id": 1,
                "title": "Введение в Python",
                "description": "Что такое Python и зачем его изучать",
                "preview": null,
                "video_url": "https://www.youtube.com/watch?v=intro",
                "course": 1
            },
            {
                "id": 2,
                "title": "Переменные и типы данных",
                "description": "Изучаем переменные и основные типы данных в Python",
                "preview": null,
                "video_url": "https://www.youtube.com/watch?v=variables",
                "course": 1
            }
        ]
    }
]
```

### Ошибка при создании урока без курса:
```json
{
    "course": [
        "Это поле обязательно."
    ]
}
```

---

## Заметки для тестирования в Postman

1. **Создайте коллекцию** "DRF LMS Homework"

2. **Создайте окружение (Environment)** с переменной:
   - `base_url`: `http://127.0.0.1:8000`

3. **Организуйте запросы в папки:**
   - Courses
   - Lessons
   - Users

4. **Для каждого запроса:**
   - Добавьте описание
   - Сохраните примеры ответов (Save Response)
   - Добавьте тесты (Tests) для проверки статус-кодов

5. **Примеры тестов в Postman:**

```javascript
// Проверка успешного создания
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

// Проверка что вернулся JSON
pm.test("Response is JSON", function () {
    pm.response.to.be.json;
});

// Проверка наличия поля id
pm.test("Response has id field", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
});
```
