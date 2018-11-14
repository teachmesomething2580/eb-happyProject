from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    # 유저 생성
    def setUp(self):
        user = User.objects.create_user(
            username='example1',
            password='asd',
            phone='+8201055555555',
            email='ex@ex1.com',
            name="KingGod"
        )
        self.user = user

    # __str__ 확인
    def test_string_representation(self):
        self.assertEqual(str(self.user), 'example1')

    # 회원가입시 500 해머 확인
    def test_first_register_500_point(self):
        self.assertEqual(self.user.hammer, 500)


class UserHammerRelationTest(TestCase):
    def setUp(self):
        user = User.objects.get(pk=1)
        self.user = user
