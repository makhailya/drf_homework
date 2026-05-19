from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson, Subscription

User = get_user_model()


class LessonTestCase(APITestCase):
    """
    Тесты для CRUD операций с уроками.
    """

    def setUp(self):
        """
        Подготовка данных для тестов.
        """
        # Создаём пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        # Создаём курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

        # Создаём урок
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

    def test_lesson_create(self):
        """
        Тест создания урока.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'video_url': 'https://www.youtube.com/watch?v=new',
            'course': self.course.id
        }

        response = self.client.post('/api/lessons/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Lesson')

    def test_lesson_create_invalid_url(self):
        """
        Тест создания урока с недопустимой ссылкой.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'video_url': 'https://vimeo.com/123456',  # Не YouTube!
            'course': self.course.id
        }

        response = self.client.post('/api/lessons/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_list(self):
        """
        Тест получения списка уроков.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/lessons/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_retrieve(self):
        """
        Тест получения конкретного урока.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/api/lessons/{self.lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_lesson_update(self):
        """
        Тест обновления урока.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Updated Lesson',
            'description': 'Updated Description'
        }

        response = self.client.patch(f'/api/lessons/{self.lesson.id}/update/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    def test_lesson_delete(self):
        """
        Тест удаления урока.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f'/api/lessons/{self.lesson.id}/delete/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_create_unauthorized(self):
        """
        Тест создания урока без авторизации.
        """
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'video_url': 'https://www.youtube.com/watch?v=new',
            'course': self.course.id
        }

        response = self.client.post('/api/lessons/', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(APITestCase):
    """
    Тесты для функционала подписки на курс.
    """

    def setUp(self):
        """
        Подготовка данных для тестов.
        """
        # Создаём пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        # Создаём курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_subscription_create(self):
        """
        Тест создания подписки.
        """
        self.client.force_authenticate(user=self.user)

        data = {'course_id': self.course.id}

        response = self.client.post('/api/subscription/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_delete(self):
        """
        Тест удаления подписки.
        """
        self.client.force_authenticate(user=self.user)

        # Сначала создаём подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Теперь удаляем
        data = {'course_id': self.course.id}
        response = self.client.post('/api/subscription/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_toggle(self):
        """
        Тест переключения подписки (добавить -> удалить -> добавить).
        """
        self.client.force_authenticate(user=self.user)

        data = {'course_id': self.course.id}

        # Первый запрос - создаём подписку
        response1 = self.client.post('/api/subscription/', data)
        self.assertEqual(response1.data['message'], 'Подписка добавлена')

        # Второй запрос - удаляем подписку
        response2 = self.client.post('/api/subscription/', data)
        self.assertEqual(response2.data['message'], 'Подписка удалена')

        # Третий запрос - снова создаём
        response3 = self.client.post('/api/subscription/', data)
        self.assertEqual(response3.data['message'], 'Подписка добавлена')

    def test_subscription_unauthorized(self):
        """
        Тест подписки без авторизации.
        """
        data = {'course_id': self.course.id}

        response = self.client.post('/api/subscription/', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseTestCase(APITestCase):
    """
    Тесты для CRUD операций с курсами.
    """

    def setUp(self):
        """
        Подготовка данных для тестов.
        """
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_course_create(self):
        """
        Тест создания курса.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'New Course',
            'description': 'New Description'
        }

        response = self.client.post('/api/courses/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_list(self):
        """
        Тест получения списка курсов.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/courses/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_course_retrieve(self):
        """
        Тест получения конкретного курса.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/api/courses/{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Course')
