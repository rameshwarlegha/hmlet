from base64 import b64decode

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

USER_REGISTER_URL = reverse('user_register')
POST_CREATE_URL = reverse('post_create')
POST_LIST_URL = reverse('post_list')
POST_BULK_UPDATE_DELETE_URL = reverse('post_bulk_update_delete')


def generate_photo_file():
    image_data = b64decode(
        "R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
    image_file = ContentFile(image_data, 'one.GIF')
    uploaded_image_file = SimpleUploadedFile(
        image_file.name,
        image_file.read(),
        content_type="image/png"
    )
    return uploaded_image_file


class PostTest(APITestCase):

    def setUp(self):
        data = {'username': 'class-user',
                'email': 'class@user.com',
                'password': 'classpass',
                'confirm_password': 'classpass'}

        response = self.client.post(USER_REGISTER_URL, data, format='json')
        self.access_token = response.json().get('access')

        self.post_data = {'caption': 'First Test Post. #successcheck #test',
                          'is_draft': False, 'image': generate_photo_file()}

        self.update_post_data = {'caption': 'Update First Post". #updatesuccess'}

    def authenticate_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )

    def test_post_create_authentication(self):
        response = self.client.post(POST_CREATE_URL, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_create_validation(self):
        self.invalid_post_data = dict()
        self.authenticate_user()
        response = self.client.post(POST_CREATE_URL, self.invalid_post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_create_execution(self):
        self.authenticate_user()
        response = self.client.post(POST_CREATE_URL, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_list_execution(self):
        self.authenticate_user()
        response = self.client.get(POST_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_update_authentication(self):
        response = self.client.put('/api/v1/photos/4/',
                                   self.update_post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_update_validation(self):
        self.authenticate_user()
        response = self.client.put('/api/v1/photos/4/',
                                   self.update_post_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_delete_authentication(self):
        response = self.client.delete('/api/v1/photos/4/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_delete_validation(self):
        self.authenticate_user()
        response = self.client.delete('/api/v1/photos/4/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)