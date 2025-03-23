from django.test import TestCase, Client
from django.contrib.auth import get_user_model  
from django.urls import reverse
from .models import Post
from django.utils import timezone
from datetime import date, timedelta, datetime

TEST_USERNAME = 'testuser2'
TEST_EMAIL = 'testuser2@gmail.com'
TEST_PASSWORD = 'occie2025'


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.post = Post.objects.create(
            author=cls.user,
            title='Test Post',
            content='This is a test post'
        )
    
    def test_post_content(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.author.username, TEST_USERNAME)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post')

    def test_post_str_method(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(str(post), f'{ post.title } is written by { post.author.username }')
        
    def test_get_absolute_url(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.get_absolute_url(), reverse('post-detail', args=[post.id]))


class PostViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)

        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post'
        )

    def test_PostListView(self):
        url = reverse('blog-home')
        response = self.client.get(url)
        # print(f'Debugging: { response.url }')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_PostListView(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        # print(f'Debugging: { response.url }')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_PostCreateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        get_response = self.client.get(reverse('post-new'))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'blog/post_form.html')

        post_response = self.client.post(reverse('post-new'), {
            'title': 'New Test Post',
            'content': 'New This is a test post'
        })
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    def test_PostUpdateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('post-update', kwargs={'pk': self.post.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'blog/post_form.html')

        self.assertEqual(self.post.title, 'Test Post')  # Check the original

        post_response = self.client.post(url, {
            'title': 'Update Test Post',
            'content': 'Update This is a test post'
         })

        self.post.refresh_from_db()
        self.assertEqual(post_response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.post.title, 'Update Test Post')

    def test_PostDeleteView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('post-delete', kwargs={'pk': self.post.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'blog/post_confirm_delete.html')

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)  # Redirect after POST
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
