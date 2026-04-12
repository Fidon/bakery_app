from apps.base_model import UUIDModel
from django.db import models
from django.conf import settings
from apps.inventory.models import SnackItem


class WasteReport(UUIDModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    snack_item = models.ForeignKey(
        SnackItem,
        on_delete=models.PROTECT,
        related_name='waste_reports'
    )
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    waste_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='waste_reports_filed'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='waste_reports_reviewed'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'waste_reports'
        ordering = ['-waste_date', '-created_at']

    def __str__(self):
        return f"{self.snack_item.name} — {self.quantity} wasted ({self.status})"