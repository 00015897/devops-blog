from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from blog.models import Category, Post


User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.category = Category.objects.create(name="DevOps")
        self.post = Post.objects.create(
            title="Test Post", content="Content", author=self.user
        )
        self.post.categories.add(self.category)

    def test_home_page_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_login_required_for_dashboard(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_for_logged_in_user(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_create_post_requires_login(self):
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 302)

    def test_many_to_many_relationship(self):
        self.assertIn(self.category, self.post.categories.all())

