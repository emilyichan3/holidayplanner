from django.test import TestCase, Client
from django.contrib.auth import get_user_model  
from django.urls import reverse
from .models import Category, Plan, Trip, Schedule

TEST_USERNAME = 'testuser2'
TEST_EMAIL = 'testuser2@gmail.com'
TEST_PASSWORD = 'occie2025'

class CategoryModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.category = Category.objects.create(
            marker=cls.user,
            category_name='Test Category',
            description='This is a test category'
        )
    
    def test_category_content(self):
        category = Category.objects.get(pk=1)
        self.assertEqual(category.marker.username, TEST_USERNAME)
        self.assertEqual(category.category_name, 'Test Category')
        self.assertEqual(category.description, 'This is a test category')

    def test_category_str_method(self):
        category = Category.objects.get(pk=1)
        self.assertEqual(str(category), f'{ category.category_name } is marked by { category.marker.username }')
        
    def test_get_absolute_url(self):
        category = Category.objects.get(pk=1)
        self.assertEqual(category.get_absolute_url(), reverse('trips-myCategory', args=[category.marker.username]))


class TripsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)

        self.category = Category.objects.create(
            marker=self.user,
            category_name='Test Category',
            description='This is a test category'
        )

    def test_MyCategoryListView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myCategory', kwargs={'username': self.user.username})
        response = self.client.get(url)
        # print(f'Debugging: { response.url }')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test category')
        self.assertTemplateUsed(response, 'trips/myCategory_list.html')

    def test_MyCategoryCreateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        get_response = self.client.get(reverse('trips-myCategory-new'))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myCategory_form.html')

        category_response = self.client.post(reverse('trips-myCategory-new'), {
            'category_name': 'New Test Category',
            'description': 'New This is a test category'
        })
        self.assertEqual(category_response.status_code, 302)
        self.assertTrue(Category.objects.filter(category_name='New Test Category').exists())

    def test_MyCategoryUpdateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myCategory-update', kwargs={'pk': self.category.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myCategory_form.html')

        self.assertEqual(self.category.category_name, 'Test Category')  # Check the original

        category_response = self.client.post(url, {
            'category_name': 'Update Test Category',
            'description': 'Update This is a test category'
         })

        self.category.refresh_from_db()
        self.assertEqual(category_response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.category.category_name, 'Update Test Category')

    def test_MyCategoryDeleteView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myCategory-delete', kwargs={'pk': self.category.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myCategory_confirm_delete.html')

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)  # Redirect after POST
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())