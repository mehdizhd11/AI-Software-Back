from django.contrib import admin
from .models import RestaurantProfile

@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'manager',
        'business_type',
        'city_name',
        'state',
        'display_score',
        'delivery_price',
    )
    search_fields = ('name', 'manager__phone_number', 'city_name') 
    list_editable = ('state',)
    list_filter = ('state', 'business_type') 
    ordering = ('name',)  

    fieldsets = (
        (None, {'fields': ('manager', 'name', 'business_type', 'city_name', 'state')}),
        ('Details', {'fields': ('delivery_price', 'address', 'description', 'display_score')}),
        ('Operating Hours', {'fields': ('open_hour', 'close_hour')}),
        ('Location', {'fields': ('latitude', 'longitude')}),
        ('Photo', {'fields': ('photo',)}),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('display_score',)

    def display_score(self, obj):
        return obj.calculate_score()

    display_score.short_description = 'Score'

