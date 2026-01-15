from django.db import models

# Create your models here.


from django.db import models
from datetime import date

class FoodItem(models.Model):
    """
    Model representing a food item added by the user.
    
    properties of this class:
        name: The name of the food item
        calories: Number of calories in the food item
        date_added: Date when the item was added by the user
        created_at: Timestamp when the item was created
        updated_at: Timestamp when the item was last updated
        is_deleted: Soft delete flag for data integrity
    """
    
    name = models.CharField(
        max_length=200,
        help_text="Name of the food item"
    )
    calories = models.PositiveIntegerField(
        help_text="Number of calories in this item"
    )
    date_added = models.DateField(
        default=date.today,
        help_text="Date when the item was added"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of creation"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last update"
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag"
    )
    
    class Meta:
        ordering = ['-date_added', '-created_at']
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"
        indexes = [
            models.Index(fields=['date_added']),
        ]
    
    def __str__(self):
        """String representation of the food item."""
        return f"{self.name} ({self.calories} kcal)"