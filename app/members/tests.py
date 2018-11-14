from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='example1',
            password='asd',
        )
        self.user = user

    def test_string_representation(self):
        self.assertEqual(str(self.user), 'example1')