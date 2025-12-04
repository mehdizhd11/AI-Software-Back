from rest_framework.exceptions import NotFound

from restaurant.models import RestaurantProfile
from .models import Order


class RestaurantResolver:
    """Resolves the restaurant profile for the authenticated user."""

    def __init__(self, user):
        self.user = user

    def get_restaurant(self) -> RestaurantProfile:
        try:
            return self.user.restaurant_profile
        except RestaurantProfile.DoesNotExist:
            raise NotFound(detail="Restaurant not found.")


class RestaurantOrderService:
    """Handles order retrieval operations scoped to a restaurant."""

    def __init__(self, restaurant: RestaurantProfile):
        self.restaurant = restaurant

    def list_orders(self):
        return Order.objects.filter(restaurant=self.restaurant)

    def get_order_by_id(self, order_id: int) -> Order:
        try:
            return Order.objects.get(restaurant=self.restaurant, order_id=order_id)
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found")
