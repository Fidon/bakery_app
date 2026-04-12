from apps.base_model import UUIDModel
from django.db import models
from django.conf import settings


class SnackItem(UUIDModel):
    UNIT_CHOICES = [
        ('piece', 'Piece'),
        ('dozen', 'Dozen'),
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('tray', 'Tray'),
        ('pack', 'Pack'),
    ]

    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='piece')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='snack_items_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'snack_items'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_unit_display()})"