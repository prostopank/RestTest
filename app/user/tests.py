from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from user.models import User


class TestUserAPIViews(APITestCase):
    def setUp(self):
        self.employee = User.objects.create_user(first_name='user2', last_name='user2', surname='user2',
                                                 email='user2@email.com', phone='+375255395566', type=User.EMPLOYEE,
                                                 username='user2', password='Pas$w0rd')
        response = self.client.post(reverse('token_obtain_pair'),
                                    {'email': 'user2@email.com', 'password': 'Pas$w0rd'})

        self.refresh = response.data.get('refresh')
        self.access = response.data.get('access')

    def test_register(self):
        data = {
            'first_name': 'user1', 'last_name': 'user1', 'surname': 'user1',
            'email': 'user1@email.com', 'phone': '+375255395555', 'type': User.CUSTOMER,
            'username': 'user1', 'password': 'Pas$w0rd', 'password2': 'Pas$w0rd'
        }
        response = self.client.post(reverse('user_register'), data)
        self.assertEqual(201, response.status_code)
        self.assertTrue(User.objects.get(email='user1@email.com'))

    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'),
                                    {'email': 'user2@email.com', 'password': 'Pas$w0rd'})
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.data.get('refresh'))
        self.assertTrue(response.data.get('access'))

    def test_refresh(self):
        response = self.client.post(reverse('token_refresh'),
                                    {'refresh': self.refresh})
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.access != response.data.get('access'))

    def test_blacklist(self):
        self.assertEqual(0, len(BlacklistedToken.objects.all()))
        response = self.client.post(reverse('token_blacklist'),
                                    {'refresh': self.refresh})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(BlacklistedToken.objects.all()))
