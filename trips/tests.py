from django.test import TestCase, Client
from django.contrib.auth import get_user_model  
from django.urls import reverse
from .models import Category, Plan, Trip, Schedule
from django.utils import timezone
from datetime import date, timedelta, datetime

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


class CategoryViewsTests(TestCase):
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


class PlanModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.category = Category.objects.create(
            marker=cls.user,
            category_name='Test Food Category',
            description='This is a test food category'
        )

        cls.plan = Plan.objects.create(
            planner=cls.user,
            plan_name='Test Plan',
            note='This is a test plan',
            country='Ireland',
            city='Dublin'
        )
        # set ManyToManyField
        cls.plan.categories.set([cls.category]) 
    
    def test_Plan_content(self):
        category = Category.objects.get(pk=1)
        plan = Plan.objects.get(pk=1)
        self.assertEqual(plan.planner.username, TEST_USERNAME)
        self.assertEqual(plan.plan_name, 'Test Plan')
        self.assertEqual(plan.country, 'Ireland')
         # Correct way to check ManyToMany relationship
        self.assertIn(category, plan.categories.all()) 

    def test_Plan_str_method(self):
        plan = Plan.objects.get(pk=1)
        self.assertEqual(str(plan), f'{ plan.plan_name } is owned by  { plan.planner.username }')
        

class PlanViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        self.category = Category.objects.create(
            marker=self.user,
            category_name='Test Food Category',
            description='This is a test food category'
        )
        category = Category.objects.get(category_name='Test Food Category')  # Get the category ID

        self.plan = Plan.objects.create(
            planner = self.user,
            plan_name='Test Plan',
            note='This is a test plan',
            country='Ireland',
            city='Dublin'
        )
        self.plan.categories.add(category)  # Associate category with the plan
        # self.plan.categories.set([self.category]) 

    def test_MyPlanListView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myPlan', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test plan')
        self.assertTemplateUsed(response, 'trips/myPlan_list.html')

    def test_MyPlanCreateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        get_response = self.client.get(reverse('trips-myPlan-new'))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myPlan_form.html')

        category_response = self.client.post(reverse('trips-myCategory-new'), {
            'category_name': 'New Test Asia Category',
            'description': 'New This is a test Asia category'
        })
        # Ensure the category was created successfully
        self.assertEqual(category_response.status_code, 302)  # 302 indicates redirection after creating the category
        category = Category.objects.get(category_name='New Test Asia Category')  # Get the category ID
        print(category)
        plan_response = self.client.post(reverse('trips-myPlan-new'), {
            'plan_name': 'New Test Plan',
            'note': 'This is a new test plan',
            'country':'IE',
            'city':'Dublin',
            'categories':[category.id]
        })
        # print(plan_response.context['form'].errors)
        self.assertEqual(plan_response.status_code, 302)
        plan = Plan.objects.get(plan_name='New Test Plan')
        self.assertIn(category, plan.categories.all())  # Check if category is linked
        self.assertTrue(Plan.objects.filter(plan_name='New Test Plan').exists())

    def test_MyPlanUpdateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myPlan-update', kwargs={'pk': self.plan.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myPlan_form.html')

        self.assertEqual(self.plan.plan_name, 'Test Plan')  # Check the original

        # Ensure at least one category exists
        category = Category.objects.create(
            marker=self.user,
            category_name='Test Category',
            description='Test category description'
        )
        self.plan.categories.add(category)  # Associate category with the plan
        
        plan_response = self.client.post(url, {
            'plan_name': 'Update Test Plan',
            'categories': [category.pk]  # Pass a list of category IDs
         })

        self.plan.refresh_from_db()
        self.assertEqual(plan_response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.plan.plan_name, 'Update Test Plan')

    def test_MyPlanDeleteView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myPlan-delete', kwargs={'pk': self.category.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myPlan_confirm_delete.html')

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)  # Redirect after POST
        self.assertFalse(Plan.objects.filter(pk=self.plan.pk).exists())

    def test_MyPlanSearchListView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myPlan-Search', kwargs={'pk': self.plan.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Plan')
        self.assertTemplateUsed(response, 'trips/myPlan_trip_seach.html')


class TripModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.trip = Trip.objects.create(
            traveler=cls.user,
            trip_name='Test Trip',
            trip_description='This is a test trip'
        )

        cls.trip = Trip.objects.create(
            traveler=cls.user,
            trip_name='Test Trip',
            trip_description='This is a test trip',
            date_fm= date.today(),
            date_to= date.today() + timedelta(days=6)
        )

    def test_Trip_content(self):
        trip = Trip.objects.get(pk=1)
        self.assertEqual(trip.traveler.username, TEST_USERNAME)
        self.assertEqual(trip.trip_name, 'Test Trip')
        self.assertEqual(trip.trip_description, 'This is a test trip')

    def test_Trip_str_method(self):
        trip = Trip.objects.get(pk=1)
        self.assertEqual(str(trip), f'{ trip.trip_name } is owned by { trip.traveler.username }')
        

class TripViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        self.trip = Trip.objects.create(
            traveler = self.user,
            trip_name='Test Trip',
            trip_description='This is a test trip',
            date_fm=date.today(),
            date_to=date.today()+ timedelta(days=6),
        )

    def test_MyTripListView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myTrip', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test trip')
        self.assertTemplateUsed(response, 'trips/myTrip_list.html')

    def test_MyTripCreateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        get_response = self.client.get(reverse('trips-myTrip-new'))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myTrip_form.html')

        trip_response = self.client.post(reverse('trips-myTrip-new'), {
            'trip_name': 'New Test Trip',
            'trip_description': 'This is a new test trip',
            'date_fm':date.today(),
            'date_to':date.today() + timedelta(days=7),
        })
        # debug tool
        # print(trip_response.context['form'].errors)
        self.assertEqual(trip_response.status_code, 302)
        self.assertTrue(Trip.objects.filter(trip_name='New Test Trip').exists())

    def test_MyTripUpdateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myTrip-update', kwargs={'pk': self.trip.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myTrip_form.html')

        self.assertEqual(self.trip.trip_name, 'Test Trip')  # Check the original
        
        trip_response = self.client.post(url, {
            'trip_name': 'Update Test Trip',
            'trip_description': 'This is a update test trip',
            'date_fm':date.today(),
            'date_to':date.today() + timedelta(days=6)
         })

        self.trip.refresh_from_db()
        # print(trip_response.context['form'].errors)
        self.assertEqual(trip_response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.trip.trip_name, 'Update Test Trip')

    def test_MyTripDeleteView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse('trips-myTrip-delete', kwargs={'pk': self.trip.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myTrip_confirm_delete.html')

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)  # Redirect after POST
        self.assertFalse(Trip.objects.filter(pk=self.trip.pk).exists())


class ScheduleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.trip = Trip.objects.create(
            traveler=cls.user,
            trip_name='Test Trip',
            trip_description='This is a test trip',
            date_fm=date.today(),
            date_to=date.today()+ timedelta(days=6),
        )

        cls.schedule = Schedule.objects.create(
            traveler=cls.user,
            destination='Test Schedule',
            scheduled_date= date.today(),
            trip=cls.trip
        )
    
    def test_Schedule_content(self):
        trip = Trip.objects.get(pk=1)
        schedule = Schedule.objects.get(pk=1)
        self.assertEqual(schedule.traveler.username, TEST_USERNAME)
        self.assertEqual(schedule.destination, 'Test Schedule')
        self.assertEqual(schedule.trip, trip)


    def test_Schedule_str_method(self):
        schedule = Schedule.objects.get(pk=1)
        self.assertEqual(str(schedule), f'{ schedule.destination } is scheduled by { schedule.traveler.username }')


class ScheduleViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD)
        self.trip = Trip.objects.create(
            traveler=self.user,
            trip_name='Test Trip',
            trip_description='This is a test trip',
            date_fm=date.today(),
            date_to=date.today()+ timedelta(days=6),
        )

        self.schedule = Schedule.objects.create(
            traveler = self.user,
            destination='Test Schedule',
            scheduled_date= date.today(),
            trip=self.trip
        )
        self.category = Category.objects.create(
            marker=self.user,
            category_name='Test Food Category',
            description='This is a test food category'
        )
        category = Category.objects.get(category_name='Test Food Category')  # Get the category ID

        self.plan = Plan.objects.create(
            planner = self.user,
            plan_name='Test Plan',
            note='This is a test plan',
            country='Ireland',
            city='Dublin'
        )
        self.plan.categories.add(category)  # Associate category with the plan

    def test_MyScheduleByTripListView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        trip = Trip.objects.get(pk=1)
        url = reverse('trips-mySchedule-by-myTrip', kwargs={'trip_id': trip.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Schedule')
        self.assertTemplateUsed(response, 'trips/myTrip_schedule_list.html')

    def test_MyScheduleByTripCreateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        trip = Trip.objects.get(pk=1)
        get_response = self.client.get(reverse('trips-mySchedule-by-myTrip-new', kwargs={'trip_id': trip.id}))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myTrip_schedule_form.html')

        schedule_response = self.client.post(reverse('trips-mySchedule-by-myTrip-new', kwargs={'trip_id': trip.id}), {
            'destination': 'New Test Schedule',
            'scheduled_date': date.today(),
            'trip': trip.id
        })
        # print(plan_response.context['form'].errors)
        self.assertEqual(schedule_response.status_code, 302)
        self.assertTrue(Schedule.objects.filter(destination='New Test Schedule').exists())

    def test_MyScheduleByTripUpdateView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        trip = Trip.objects.get(pk=1)
        url = reverse('trips-mySchedule-by-myTrip-update', kwargs={ 'trip_id': trip.id, 'pk': self.schedule.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myTrip_schedule_form.html')

        self.assertEqual(self.schedule.destination, 'Test Schedule')  # Check the original

        schedule_response = self.client.post(url, {
            'destination': 'Update Test Schedule',
            'scheduled_date': date.today(),
            'trip': trip.id  # Pass a list of category IDs
         })

        self.schedule.refresh_from_db()
        self.assertEqual(schedule_response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.schedule.destination, 'Update Test Schedule')

    def test_MyScheduleByTripDeleteView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        trip = Trip.objects.get(pk=1)    
        url = reverse('trips-mySchedule-by-myTrip-delete', kwargs={ 'trip_id': trip.id, 'pk': self.schedule.pk})        
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myTrip_schedule_delete.html')

        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, 302)  # Redirect after POST
        self.assertFalse(Schedule.objects.filter(pk=self.schedule.pk).exists())

    def test_MyScheduleSearchByMyPlanListView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        trip = Trip.objects.get(pk=1)
        url = reverse('trips-mySchedule-Search', kwargs={'trip_id': trip.id, 'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Schedule')
        self.assertTemplateUsed(response, 'trips/myTrip_schedule_seach.html')

    def test_MyScheduleSearchByMyPlanListView(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        trip = Trip.objects.get(pk=1)
        plan = Plan.objects.get(pk=1)
        get_response = self.client.get(reverse('trips-myPlan-Convert-new', kwargs={'trip_id': trip.id, 'plan_id': plan.id}))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'trips/myTrip_schedule_form.html')

        schedule_response = self.client.post(reverse('trips-myPlan-Convert-new', kwargs={'trip_id': trip.id, 'plan_id': plan.id}), {
            'destination': plan.plan_name,
            'scheduled_date': date.today(),
            'trip': trip.id
        })
        # print(schedule_response.context['form'].errors)
        self.assertEqual(schedule_response.status_code, 302)
        self.assertTrue(Schedule.objects.filter(destination='Test Plan').exists())
