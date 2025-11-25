from typing import Mapping, MutableMapping
from customer.models import CustomerProfile
from restaurant.models import RestaurantProfile
from user.models import User


# Apply a Service/Factory pattern for user registration:
# a service dispatches on a role (customer vs. restaurant manager) and delegates creation to role-specific handlers.
# This centralizes shared steps (e.g., unique phone-number check, creating User)
# while keeping each role’s specifics (profile model and default state).
# The API responses and serializers remain the same; only the creation logic moves to the service layer.


def _register_customer(data: MutableMapping | Mapping) -> User:
    payload = dict(data)
    state = payload.pop('state', 'approved')
    user = User.objects.create_user(**payload, role='customer')
    CustomerProfile.objects.create(user=user, state=state)
    return user


def _register_restaurant_manager(data: MutableMapping | Mapping) -> User:
    payload = dict(data)
    name = payload.pop('name')
    business_type = payload.pop('business_type')
    city_name = payload.pop('city_name')
    state = 'pending'

    manager = User.objects.create_user(**payload, role='restaurant_manager')
    RestaurantProfile.objects.create(
        manager=manager,
        name=name,
        business_type=business_type,
        city_name=city_name,
        state=state,
    )
    return manager


def register_user(role: str, data: MutableMapping | Mapping) -> User:
    if role == 'customer':
        return _register_customer(data)
    if role == 'restaurant_manager':
        return _register_restaurant_manager(data)
    raise ValueError(f"Unsupported role: {role}")
