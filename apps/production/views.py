import json
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.db import transaction
from apps.inventory.models import SnackItem
from .models import ProductionLog
from .forms import ProductionBatchForm


class ProductionHistoryView(LoginRequiredMixin, ListView):
    model = ProductionLog
    template_name = 'production/history.html'
    context_object_name = 'logs'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in ('admin', 'production'):
            from django.contrib import messages
            messages.error(request, 'You do not have permission to view production history.')
            from django.shortcuts import redirect
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = ProductionLog.objects.select_related(
            'snack_item', 'logged_by'
        ).order_by('-production_date', '-created_at')

        # Admin sees all; production staff see only their own logs
        if self.request.user.role == 'production':
            qs = qs.filter(logged_by=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active_items'] = SnackItem.objects.filter(
            is_active=True
        ).order_by('name')
        return ctx


@login_required
def production_log_view(request):
    """
    GET  — render the logging page with active snack items for the cart.
    POST — receive a JSON batch of {snack_item, quantity, notes} rows,
           validate each, save all or none (atomic), update stock.
    """
    if request.user.role not in ('admin', 'production'):
        from django.contrib import messages
        messages.error(request, 'You do not have permission to log production.')
        from django.shortcuts import redirect
        return redirect('accounts:dashboard')

    if request.method == 'GET':
        from django.shortcuts import render
        context = {
            'active_items': SnackItem.objects.filter(
                is_active=True
            ).order_by('name'),
            'today': date.today().isoformat(),
        }
        return render(request, 'production/log.html', context)

    # POST — process batch
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse(
            {'success': False, 'error': 'Invalid request format.'}, status=400
        )

    production_date = body.get('production_date')
    rows = body.get('rows', [])

    if not production_date:
        return JsonResponse(
            {'success': False, 'error': 'Production date is required.'}, status=400
        )

    if not rows:
        return JsonResponse(
            {'success': False, 'error': 'Add at least one item to the batch.'}, status=400
        )

    if len(rows) > 50:
        return JsonResponse(
            {'success': False, 'error': 'Maximum 50 items per batch.'}, status=400
        )

    # Validate all rows first before saving anything
    validated = []
    seen_ids = set()

    for i, row in enumerate(rows):
        form = ProductionBatchForm(row)
        if not form.is_valid():
            first_error = list(form.errors.values())[0][0]
            return JsonResponse(
                {'success': False, 'error': f'Row {i + 1}: {first_error}'}, status=400
            )
        item = form.cleaned_data['snack_item']
        if str(item.pk) in seen_ids:
            return JsonResponse(
                {
                    'success': False,
                    'error': f'"{item.name}" appears more than once in this batch. Combine the quantities into one row.'
                },
                status=400
            )
        seen_ids.add(str(item.pk))
        validated.append({
            'item': item,
            'quantity': form.cleaned_data['quantity'],
            'notes': form.cleaned_data.get('notes', ''),
        })

    # Save atomically — all rows or none
    try:
        with transaction.atomic():
            for entry in validated:
                ProductionLog.objects.create(
                    snack_item=entry['item'],
                    quantity=entry['quantity'],
                    production_date=production_date,
                    notes=entry['notes'],
                    logged_by=request.user,
                )
                # Update stock
                SnackItem.objects.filter(pk=entry['item'].pk).update(
                    current_stock=entry['item'].current_stock + entry['quantity']
                )
    except Exception:
        return JsonResponse(
            {'success': False, 'error': 'Failed to save batch. Please try again.'}, status=500
        )

    count = len(validated)
    return JsonResponse({
        'success': True,
        'message': f'Production batch saved — {count} item{"s" if count != 1 else ""} logged successfully.',
    })


@login_required
def production_delete(request, pk):
    """
    Admin only. Deletes a production log entry and reverses the stock change.
    """
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    log = get_object_or_404(ProductionLog, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=405)

    try:
        with transaction.atomic():
            # Reverse the stock addition
            SnackItem.objects.filter(pk=log.snack_item.pk).update(
                current_stock=max(0, log.snack_item.current_stock - log.quantity)
            )
            log.delete()
    except Exception:
        return JsonResponse(
            {'success': False, 'error': 'Failed to delete entry. Please try again.'}, status=500
        )

    return JsonResponse({
        'success': True,
        'message': 'Production log entry deleted and stock reversed.'
    })