from typing import Mapping, MutableMapping, Protocol
from customer.models import CustomerProfile
from restaurant.models import RestaurantProfile
from user.models import User


# Apply a Service/Factory pattern for user registration:
# a service dispatches on a role (customer vs. restaurant manager) and delegates creation to role-specific handlers.
# This centralizes shared steps (e.g., unique phone-number check, creating User)
# while keeping each role’s specifics (profile model and default state).
# The API responses and serializers remain the same; only the creation logic moves to the service layer.


class RegistrationStrategy(Protocol):
    def register(self, data: MutableMapping | Mapping) -> User:
        ...


class _CustomerRegistrationStrategy:
    def register(self, data: MutableMapping | Mapping) -> User:
        payload = dict(data)
        state = payload.pop('state', 'approved')
        user = User.objects.create_user(**payload, role='customer')
        CustomerProfile.objects.create(user=user, state=state)
        return user


class _RestaurantManagerRegistrationStrategy:
    def register(self, data: MutableMapping | Mapping) -> User:
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


class RegistrationService(Protocol):
    def register_user(self, role: str, data: MutableMapping | Mapping) -> User:
        ...


class DefaultRegistrationService:
    def __init__(self, strategies: Mapping[str, RegistrationStrategy] | None = None):
        self._strategies = strategies or {
            'customer': _CustomerRegistrationStrategy(),
            'restaurant_manager': _RestaurantManagerRegistrationStrategy(),
        }

    def register_user(self, role: str, data: MutableMapping | Mapping) -> User:
        try:
            strategy = self._strategies[role]
        except KeyError:
            raise ValueError(f"Unsupported role: {role}")

        return strategy.register(data)


default_registration_service = DefaultRegistrationService()


def register_user(role: str, data: MutableMapping | Mapping) -> User:
    return default_registration_service.register_user(role, data)
