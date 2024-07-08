from rest_framework.test import APITestCase
from django.urls import reverse

from user.models import User
from task.models import Task


class TestTaskAPIViews(APITestCase):
    def setUp(self):
        self.url_list = reverse('task_list')
        self.url_create = reverse('task_create')

        self.customer = User.objects.create_user(first_name='user1', last_name='user1', surname='user1',
                                                 email='user1@email.com', phone='+375255395555', type=User.CUSTOMER,
                                                 username='user1', password='Pas$w0rd')
        self.employee = User.objects.create_user(first_name='user2', last_name='user2', surname='user2',
                                                 email='user2@email.com', phone='+375255395566', type=User.EMPLOYEE,
                                                 username='user2', password='Pas$w0rd')
        access_token_response = self.client.post(reverse('token_obtain_pair'),
                                                 {'email': 'user1@email.com', 'password': 'Pas$w0rd'})
        self.access_token_user1 = access_token_response.data.get('access')
        access_token_response = self.client.post(reverse('token_obtain_pair'),
                                                 {'email': 'user2@email.com', 'password': 'Pas$w0rd'})
        self.access_token_user2 = access_token_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_user1}')

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(200, response.status_code)

    def test_create(self):
        self.assertEqual(0, len(Task.objects.all()))
        response = self.client.post(self.url_create, {'name': 'task1'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(Task.objects.all()))

    def test_assign(self):
        response = self.client.post(self.url_create, {'name': 'task1'})
        response = self.client.put(reverse('task_assign', args=[Task.objects.get(customer=self.customer).id]))
        self.assertEqual(400, response.status_code)
        self.assertEqual(Task.objects.get(customer=self.customer).employee, None)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_user2}')

        response = self.client.put(reverse('task_assign', args=[Task.objects.get(customer=self.customer).id]))
        self.assertEqual(200, response.status_code)
        self.assertEqual(Task.objects.get(customer=self.customer).employee, self.employee)
        self.assertEqual(Task.objects.get(customer=self.customer).status, Task.IN_PROGRESS)

    def test_complete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_user1}')
        response = self.client.post(self.url_create, {'name': 'task1'})
        self.assertEqual(Task.objects.get(customer=self.customer).employee, None)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_user2}')
        response = self.client.put(reverse('task_assign', args=[Task.objects.get(customer=self.customer).id]))
        self.assertEqual(200, response.status_code)
        response = self.client.put(
            reverse('task_complete', args=[Task.objects.get(customer=self.customer).id]), {'report': 'report1'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Task.objects.get(customer=self.customer).employee, self.employee)
        self.assertEqual(Task.objects.get(customer=self.customer).report, 'report1')
        self.assertEqual(Task.objects.get(customer=self.customer).status, Task.COMPLETED)
