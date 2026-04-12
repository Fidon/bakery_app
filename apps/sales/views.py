import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import ListView, DetailView

from apps.inventory.models import SnackItem
from .models import SaleTransaction, SaleTransactionItem
from .forms import SaleItemForm


def _sales_access(user):
    return user.role in ('admin', 'sales')


class SaleHistoryView(LoginRequiredMixin, ListView):
    model = SaleTransaction
    template_name = 'sales/history.html'
    context_object_name = 'transactions'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not _sales_access(request.user):
            messages.error(request, 'You do not have permission to view sales history.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = SaleTransaction.objects.select_related('sold_by').order_by(
            '-sale_date', '-created_at'
        )
        # Sales staff see only their own transactions
        if self.request.user.role == 'sales':
            qs = qs.filter(sold_by=self.request.user)
        return qs


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = SaleTransaction
    template_name = 'sales/detail.html'
    context_object_name = 'transaction'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not _sales_access(request.user):
            messages.error(request, 'Permission denied.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = get_object_or_404(SaleTransaction, pk=self.kwargs['pk'])
        # Sales staff can only view their own transactions
        if self.request.user.role == 'sales' and obj.sold_by != self.request.user:
            messages.error(self.request, 'You can only view your own transactions.')
            return None
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect('sales:history')
        ctx = self.get_context_data(object=self.object)
        ctx['items'] = self.object.items.select_related('snack_item').all()
        return self.render_to_response(ctx)


@login_required
def sale_new(request):
    if not _sales_access(request.user):
        messages.error(request, 'You do not have permission to process sales.')
        return redirect('accounts:dashboard')

    if request.method == 'GET':
        context = {
            'active_items': SnackItem.objects.filter(
                is_active=True
            ).order_by('name'),
            'today': date.today().isoformat(),
        }
        return render(request, 'sales/new.html', context)

    # POST — process cart
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse(
            {'success': False, 'error': 'Invalid request format.'}, status=400
        )

    sale_date = body.get('sale_date')
    rows = body.get('rows', [])
    notes = body.get('notes', '').strip()

    if not sale_date:
        return JsonResponse(
            {'success': False, 'error': 'Sale date is required.'}, status=400
        )
    if not rows:
        return JsonResponse(
            {'success': False, 'error': 'Add at least one item to the cart.'}, status=400
        )
    if len(rows) > 50:
        return JsonResponse(
            {'success': False, 'error': 'Maximum 50 items per transaction.'}, status=400
        )

    # Validate all rows first
    validated = []
    seen_ids = set()

    for i, row in enumerate(rows):
        form = SaleItemForm(row)
        if not form.is_valid():
            first_error = list(form.errors.values())[0][0]
            return JsonResponse(
                {'success': False, 'error': f'Row {i + 1}: {first_error}'}, status=400
            )
        item = form.cleaned_data['snack_item']
        quantity = form.cleaned_data['quantity']

        if str(item.pk) in seen_ids:
            return JsonResponse(
                {
                    'success': False,
                    'error': f'"{item.name}" appears more than once. Combine into one row.'
                },
                status=400
            )
        seen_ids.add(str(item.pk))

        # Stock check — refresh from DB to get latest value
        item.refresh_from_db()
        if item.current_stock < quantity:
            return JsonResponse(
                {
                    'success': False,
                    'error': (
                        f'Not enough stock for "{item.name}". '
                        f'Requested: {quantity}, available: {item.current_stock}.'
                    )
                },
                status=400
            )

        validated.append({
            'item': item,
            'quantity': quantity,
            'unit_price': item.price,
            'subtotal': item.price * quantity,
        })

    # Save atomically
    try:
        with transaction.atomic():
            sale = SaleTransaction.objects.create(
                sale_date=sale_date,
                notes=notes,
                sold_by=request.user,
            )
            for entry in validated:
                SaleTransactionItem.objects.create(
                    transaction=sale,
                    snack_item=entry['item'],
                    quantity=entry['quantity'],
                    unit_price=entry['unit_price'],
                )
                # Deduct stock
                SnackItem.objects.filter(pk=entry['item'].pk).update(
                    current_stock=entry['item'].current_stock - entry['quantity']
                )
            # Recalculate and save total
            sale.recalculate_total()

    except Exception:
        return JsonResponse(
            {'success': False, 'error': 'Failed to save transaction. Please try again.'},
            status=500
        )

    return JsonResponse({
        'success': True,
        'message': f'Transaction {sale.transaction_ref} saved successfully.',
        'redirect_url': f'/sales/{sale.pk}/detail/',
    })


@login_required
def get_item_price(request, pk):
    """Ajax endpoint — returns item price and current stock for cart display."""
    if not _sales_access(request.user):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)
    item = get_object_or_404(SnackItem, pk=pk, is_active=True)
    return JsonResponse({
        'success': True,
        'price': str(item.price),
        'current_stock': item.current_stock,
        'unit': item.get_unit_display(),
    })


@login_required
def sale_cancel(request, pk):
    """Admin only. Cancels a transaction and restores stock."""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=405)

    sale = get_object_or_404(SaleTransaction, pk=pk)

    if sale.status == 'cancelled':
        return JsonResponse(
            {'success': False, 'error': 'This transaction is already cancelled.'}, status=400
        )

    try:
        with transaction.atomic():
            for item_line in sale.items.select_related('snack_item').all():
                SnackItem.objects.filter(pk=item_line.snack_item.pk).update(
                    current_stock=item_line.snack_item.current_stock + item_line.quantity
                )
            sale.status = 'cancelled'
            sale.save(update_fields=['status'])
    except Exception:
        return JsonResponse(
            {'success': False, 'error': 'Failed to cancel transaction. Please try again.'},
            status=500
        )

    return JsonResponse({
        'success': True,
        'message': f'Transaction {sale.transaction_ref} has been cancelled and stock restored.'
    })