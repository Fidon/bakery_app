from apps.base_model import UUIDModel
from django.db import models
from django.conf import settings
from apps.inventory.models import SnackItem


class ProductionLog(UUIDModel):
    snack_item = models.ForeignKey(
        SnackItem,
        on_delete=models.PROTECT,
        related_name='production_logs'
    )
    quantity = models.PositiveIntegerField()
    production_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='production_logs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'production_logs'
        ordering = ['-production_date', '-created_at']

    def __str__(self):
        return f"{self.snack_item.name} — {self.quantity} on {self.production_date}"