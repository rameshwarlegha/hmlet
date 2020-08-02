from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

USER_REGISTER_URL = reverse('user_register')
USER_TOKEN_URL = reverse('token_obtain_pair')
USER_REFRESH_TOKEN_URL = reverse('token_refresh')


class AccountsTest(APITestCase):
    USER_REGISTER_DATA = {'username': 'class-user',
                          'email': 'class@user.com',
                          'password': 'classpass',
                          'confirm_password': 'classpass'}

    USER_CREDENTIALS = {
        'username': 'class-user',
        'password': 'classpass'
    }

    def test_successful_create_user(self):
        data = {'username': 'test-user1',
                'email': 'test@user1.com',
                'password': 'testpass1',
                'confirm_password': 'testpass1'}

        response = self.client.post(USER_REGISTER_URL, data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test-user1')

    def test_unsuccessful_create_user(self):
        data = {'username': 'test-user1',
                'email': 'test@user1.com',
                'password': 'testpass1',
                'confirm_password': 'testpass2'}

        response = self.client.post(USER_REGISTER_URL, data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.json())

    def test_successful_get_token(self):
        self.client.post(USER_REGISTER_URL, self.USER_REGISTER_DATA,
                         format='json')
        response = self.client.post(USER_TOKEN_URL,
                                    self.USER_CREDENTIALS,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.json())
        self.assertTrue('refresh' in response.json())

    def test_unsuccessful_get_token(self):
        self.client.post(USER_REGISTER_URL, self.USER_REGISTER_DATA,
                         format='json')
        user_data = self.USER_CREDENTIALS
        invalid_user_credentials = user_data.update({'password': 'random'})

        response = self.client.post(USER_TOKEN_URL,
                                    invalid_user_credentials,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_refresh_token(self):
        registration_response = self.client.post(USER_REGISTER_URL,
                                                 self.USER_REGISTER_DATA,
                                                 format='json')
        refresh_token = registration_response.json()['refresh']
        access_token = registration_response.json()['access']

        response = self.client.post(USER_REFRESH_TOKEN_URL,
                                    {'refresh': refresh_token},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.json())
        self.assertNotEqual(response.json()['access'], access_token)

    def test_unsuccessful_refresh_token(self):
        self.client.post(USER_REGISTER_URL, self.USER_REGISTER_DATA,
                         format='json')
        invalid_refresh_token = 'sdhgfjsdgfsdkjfhsdkfhsk'

        response = self.client.post(USER_REFRESH_TOKEN_URL,
                                    {'refresh': invalid_refresh_token},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
