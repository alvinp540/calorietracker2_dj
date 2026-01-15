
from django.contrib import messages
from django.db.models import Sum
from datetime import date, timedelta
from .models import FoodItem
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

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

@require_http_methods(["GET", "POST"])
def add_food(request):
    """
    Handle adding a new food item.
    
    GET: Display the form to add a food item
    POST: Process the form and create a new food item
    
        
    Returns:
        GET: Rendered add_food.html form
        POST: Redirect to index on success
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        calories = request.POST.get('calories', '').strip()
        
        # Validation
        errors = []
        
        if not name:
            errors.append('Food name is required.')
        elif len(name) > 200:
            errors.append('Food name must be less than 200 characters.')
        
        if not calories:
            errors.append('Calories are required.')
        else:
            try:
                calories = int(calories)
                if calories < 0:
                    errors.append('Calories must be a positive number.')
                elif calories > 999999:
                    errors.append('Calories value is too large.')
            except ValueError:
                errors.append('Calories must be a valid number.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'add_food.html', {
                'name': name,
                'calories': calories if isinstance(calories, int) else '',
            })
        
        # Create new food item
        FoodItem.objects.create(
            name=name,
            calories=int(calories),
            date_added=date.today()
        )
        
        messages.success(request, f'Added "{name}" ({calories} kcal) successfully!')
        return redirect('calorie_tracker:index')
    
    return render(request, 'add_food.html')


@require_http_methods(["GET", "POST"])
def edit_food(request, food_id):
    """
    Handle editing an existing food item.
    
    GET: Display the form with current values
    POST: Process the form and update the food item
   
    Returns:
        GET: Rendered edit_food.html form
        POST: Redirect to index on success
    """
    food = get_object_or_404(FoodItem, id=food_id, is_deleted=False)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        calories = request.POST.get('calories', '').strip()
        
        # Validation
        errors = []
        
        if not name:
            errors.append('Food name is required.')
        elif len(name) > 200:
            errors.append('Food name must be less than 200 characters.')
        
        if not calories:
            errors.append('Calories are required.')
        else:
            try:
                calories = int(calories)
                if calories < 0:
                    errors.append('Calories must be a positive number.')
                elif calories > 999999:
                    errors.append('Calories value is too large.')
            except ValueError:
                errors.append('Calories must be a valid number.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'edit_food.html', {
                'food': food,
                'name': name,
                'calories': calories if isinstance(calories, int) else '',
            })
        
        # Update food item
        old_name = food.name
        food.name = name
        food.calories = int(calories)
        food.save()
        
        messages.success(request, f'Updated "{old_name}" to "{name}" ({calories} kcal)!')
        return redirect('calorie_tracker:index')
    
    return render(request, 'edit_food.html', {'food': food})

@require_http_methods(["POST"])
def delete_food(request, food_id):
    """
    Handle deleting a food item (soft delete).
        
    Returns:
        Redirect to index
    """
    food = get_object_or_404(FoodItem, id=food_id, is_deleted=False)
    food_name = food.name
    
    # Soft delete
    food.is_deleted = True
    food.save()
    
    messages.success(request, f'Deleted "{food_name}" successfully!')
    return redirect('calorie_tracker:index')