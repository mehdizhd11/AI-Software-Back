from django.test import TestCase

from customer.models import CustomerProfile
from restaurant.models import RestaurantProfile
from user.models import User
from user.services.registration import register_user


class RegistrationServiceTests(TestCase):

    def test_register_customer_creates_approved_profile(self):
        data = {
            'phone_number': '1234567890',
            'password': 'strong-password',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        user = register_user('customer', data)

        self.assertIsInstance(user, User)
        self.assertEqual(user.role, 'customer')

        profile = CustomerProfile.objects.get(user=user)
        self.assertEqual(profile.state, 'approved')
        self.assertEqual(profile.user, user)

    def test_register_restaurant_manager_creates_pending_profile(self):
        data = {
            'phone_number': '0987654321',
            'password': 'strong-password',
            'name': 'Test Restaurant',
            'business_type': 'restaurant',
            'city_name': 'Test City',
        }

        manager = register_user('restaurant_manager', data)

        self.assertIsInstance(manager, User)
        self.assertEqual(manager.role, 'restaurant_manager')

        profile = RestaurantProfile.objects.get(manager=manager)
        self.assertEqual(profile.state, 'pending')
        self.assertEqual(profile.name, 'Test Restaurant')
        self.assertEqual(profile.business_type, 'restaurant')
        self.assertEqual(profile.city_name, 'Test City')
        self.assertEqual(profile.manager, manager)
