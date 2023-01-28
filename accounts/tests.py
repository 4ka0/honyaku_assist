from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testpassword1234"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="supertestuser",
            email="supertestuser@email.com",
            password="testpassword1234"
        )
        self.assertEqual(admin_user.username, "supertestuser")
        self.assertEqual(admin_user.email, "supertestuser@email.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
