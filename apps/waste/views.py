from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import transaction

from apps.accounts.mixins import admin_required
from apps.waste.models import WasteReport
from apps.waste.forms import WasteReportForm
from apps.inventory.models import SnackItem


@login_required
def report_view(request):
    """GET: render report form. POST: save waste report (production/sales only)."""
    if request.user.role == 'admin':
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'Admins cannot submit waste reports.')
        return redirect('waste:pending')

    active_items = SnackItem.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        form = WasteReportForm(request.POST)
        if form.is_valid():
            snack_item = form.cleaned_data['snack_item']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']
            waste_date = form.cleaned_data['waste_date']

            WasteReport.objects.create(
                snack_item=snack_item,
                quantity=quantity,
                reason=reason,
                waste_date=waste_date,
                reported_by=request.user,
                status='pending',
            )
            return JsonResponse({'success': True, 'message': 'Waste report submitted successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'waste/report.html', {'active_items': active_items})


@login_required
def history_view(request):
    """Waste history — admin sees all; production/sales see own department."""
    user = request.user

    if user.role == 'admin':
        reports = WasteReport.objects.select_related(
            'snack_item', 'reported_by', 'reviewed_by'
        ).order_by('-waste_date', '-created_at')
    else:
        # Same role = same department
        reports = WasteReport.objects.filter(
            reported_by__role=user.role
        ).select_related(
            'snack_item', 'reported_by', 'reviewed_by'
        ).order_by('-waste_date', '-created_at')

    return render(request, 'waste/history.html', {'reports': reports})


@admin_required
def pending_view(request):
    """Admin only — list of pending waste reports."""
    reports = WasteReport.objects.filter(
        status='pending'
    ).select_related('snack_item', 'reported_by').order_by('-created_at')

    return render(request, 'waste/pending.html', {'reports': reports})


@admin_required
@require_POST
def review_view(request, pk):
    """Admin only — approve or reject a pending waste report."""
    report = get_object_or_404(WasteReport, pk=pk, status='pending')
    action = request.POST.get('action')  # 'approve' or 'reject'

    if action not in ('approve', 'reject'):
        return JsonResponse({'success': False, 'error': 'Invalid action.'})

    if action == 'approve':
        with transaction.atomic():
            # Lock the snack item row to prevent race conditions
            item = SnackItem.objects.select_for_update().get(pk=report.snack_item_id)

            if item.current_stock < report.quantity:
                return JsonResponse({
                    'success': False,
                    'error': (
                        f'Cannot approve — current stock is {item.current_stock} '
                        f'but waste quantity is {report.quantity}. '
                        f'Stock cannot go below zero.'
                    )
                })

            SnackItem.objects.filter(pk=item.pk).update(
                current_stock=item.current_stock - report.quantity
            )
            report.status = 'approved'
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.admin_notes = request.POST.get('admin_notes', '').strip()
            report.save()

        return JsonResponse({'success': True, 'message': 'Waste report approved and stock updated.'})

    else:  # reject
        report.status = 'rejected'
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.admin_notes = request.POST.get('admin_notes', '').strip()
        report.save()
        return JsonResponse({'success': True, 'message': 'Waste report rejected.'})