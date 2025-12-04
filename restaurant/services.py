from django.db.models import Avg

from order.models import Order, OrderItem, Review


class ScoreCalculator:
    """Encapsulates score calculations for restaurants and items."""

    @staticmethod
    def calculate_restaurant_score(restaurant) -> float:
        reviews = Review.objects.filter(order__restaurant=restaurant)
        avg_score = reviews.aggregate(average=Avg('score'))['average']
        return round(avg_score, 2) if avg_score else 0.0

    @staticmethod
    def calculate_item_score(item) -> float:
        order_items = OrderItem.objects.filter(item=item)
        orders = Order.objects.filter(order_id__in=order_items.values_list('order_id', flat=True))
        avg_score = Review.objects.filter(order__in=orders).aggregate(average=Avg('score'))['average']
        return round(avg_score, 2) if avg_score else 0.0
