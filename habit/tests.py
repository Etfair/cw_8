from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.maxDiff = None
        self.user = User.objects.create(
            email='test1@test.com',
            chat_id=123
        )
        self.user.set_password('test1')

        self.another_user = User.objects.create(
            email='test2@test.com',
            chat_id=123
        )
        self.another_user.set_password('test2')

        self.pleasant_habit = Habit.objects.create(place='TestPlace1',
                                                   time='07:00',
                                                   action='Action',
                                                   award=None,
                                                   sign_pleasant_habit=True,
                                                   time_to_complete=100,
                                                   period=1,
                                                   related_habit=False,
                                                   owner=self.user,
                                                   is_published=True)

        self.pleasant_habit = Habit.objects.create(place='TestPlace1',
                                                   time='07:00',
                                                   action='Action2',
                                                   award=None,
                                                   sign_pleasant_habit=True,
                                                   time_to_complete=100,
                                                   period=1,
                                                   related_habit=False,
                                                   owner=self.user,
                                                   is_published=False)

    def test_habit_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/habit/', {'place': 'TestPlace',
                        'time': '21:00',
                        'related_habit': 'true',
                        'action': 'Action1',
                        'time_to_complete': 100}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_pleasant_habit_fail_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/habit/', {'place': 'TestPlace',
                                                'time': '21:00',
                                                'sign_pleasant_habit': 'true',
                                                'action': 'Action',
                                                'time_to_complete': 100}
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_pleasant_habit_fail_create_1(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/habit/', {'place': 'TestPlace',
                                                'time': '21:00',
                                                'related_habit': 'true',
                                                'action': 'Action1',
                                                'time_to_complete': 130})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_pleasant_habit(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/habit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_pleasant_habit(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('habit:habit-detail', kwargs={'pk': self.pleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class HabitSerializerValidator(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com',
                                        chat_id=1)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('habit:habit-list')
        self.habit = Habit.objects.create(time='15:25:00',
                                          action='умыться',
                                          place='Дом',
                                          sign_pleasant_habit=True)

    def test_time_to_complete_is_more_120(self):
        habit = Habit.objects.create(time='15:25:00',
                                     action='умыться',
                                     place='Дом',
                                     sign_pleasant_habit=True,
                                     time_to_complete=130)
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_is_more_than_seven(self):
        habit = Habit.objects.create(time='15:25:00',
                                     action='умыться',
                                     place='Дом',
                                     sign_pleasant_habit=True,
                                     period=8)
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_can_not_be_non_pleasant_habit(self):
        data = {"time": "15:25:00", "action": "умыться", "place": "Дом", "sign_pleasant_habit": True,
                "related_habit": self.habit.pk}
        response = self.client.post(self.url, data=data)
        expected_response = "{'related_habit': [ErrorDetail(string='Must be a valid boolean.', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_related_habit_and_award(self):
        data = {"time": "15:25:00", "action": "умыться", "place": "Дом", "award": "award",
                "sign_pleasant_habit": True, "related_habit": self.habit.pk}
        response = self.client.post(self.url, data=data)
        expected_response = "{'related_habit': [ErrorDetail(string='Must be a valid boolean.', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_pleasant_habit_and_related_habit(self):
        data = {"time": "15:25:00", "action": "умыться", "place": "Дом",
                "related_habit": self.habit.pk, "is_pleasant_habit": True}
        response = self.client.post(self.url, data=data)
        expected_response = "{'related_habit': [ErrorDetail(string='Must be a valid boolean.', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)


class PublishedHabitSerializerValidator(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com',
                                        chat_id=1)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('habit:public_list')
        self.maxDiff = None

    def test_PublicHabitsListAPIView(self):
        Habit.objects.create(time='15:25:00',
                             action='умыться',
                             place='Дом',
                             sign_pleasant_habit=True,
                             is_published=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
