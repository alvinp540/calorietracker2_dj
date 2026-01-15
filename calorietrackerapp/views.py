from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Sum
from datetime import date, timedelta
from .models import FoodItem

# Create your views here.
def index(request):
    """
    Main page displaying today's food items and total calorie count.
    
    Args:
        request: HttpRequest object
        
    Returns:
        Rendered index.html with food items and statistics
    """
    today = date.today()
    
    # Get all food items added today (non-deleted)
    food_items = FoodItem.objects.filter(
        date_added=today,
        is_deleted=False
    ).order_by('-created_at')
    
    # Calculate total calories for today
    total_calories = food_items.aggregate(
        total=Sum('calories')
    )['total'] or 0
    
    # Get statistics for the week
    week_ago = today - timedelta(days=7)
    weekly_data = {}
    for i in range(7, -1, -1):
        day = today - timedelta(days=i)
        daily_total = FoodItem.objects.filter(
            date_added=day,
            is_deleted=False
        ).aggregate(total=Sum('calories'))['total'] or 0
        weekly_data[day.strftime('%a')] = daily_total
    
    context = {
        'food_items': food_items,
        'total_calories': total_calories,
        'today': today,
        'weekly_data': weekly_data,
        'item_count': food_items.count(),
    }
    
    return render(request, 'index.html', context)

