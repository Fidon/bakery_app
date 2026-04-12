from apps.base_model import UUIDModel
from django.db import models
from django.conf import settings
from apps.inventory.models import SnackItem


class SaleTransaction(UUIDModel):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    transaction_ref = models.CharField(max_length=20, unique=True, editable=False)
    sale_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True, null=True)
    sold_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sale_transactions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sale_transactions'
        ordering = ['-sale_date', '-created_at']

    def __str__(self):
        return f"Sale {self.transaction_ref} — TZS {self.total_amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_ref:
            import datetime, random, string
            date_str = datetime.date.today().strftime('%Y%m%d')
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.transaction_ref = f"TXN-{date_str}-{rand_str}"
        super().save(*args, **kwargs)

    def recalculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])


class SaleTransactionItem(models.Model):
    transaction = models.ForeignKey(
        SaleTransaction,
        on_delete=models.CASCADE,
        related_name='items'
    )
    snack_item = models.ForeignKey(
        SnackItem,
        on_delete=models.PROTECT,
        related_name='sale_items'
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'sale_transaction_items'

    def __str__(self):
        return f"{self.snack_item.name} x{self.quantity} @ {self.unit_price}"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)