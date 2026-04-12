from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.db.models import Sum, Count

from apps.accounts.mixins import admin_required, production_required, sales_required
from apps.accounts.models import CustomUser
from apps.inventory.models import SnackItem
from apps.production.models import ProductionLog
from apps.sales.models import SaleTransaction
from apps.waste.models import WasteReport


def _parse_filters(request, *keys):
    return {k: request.GET.get(k, '').strip() for k in keys}


def _date_range_filter(qs, field, date_from, date_to):
    if date_from:
        parsed = parse_date(date_from)
        if parsed:
            qs = qs.filter(**{f'{field}__gte': parsed})
    if date_to:
        parsed = parse_date(date_to)
        if parsed:
            qs = qs.filter(**{f'{field}__lte': parsed})
    return qs


@production_required
def production_report(request):
    f = _parse_filters(request, 'date_from', 'date_to', 'user_id', 'item_id')

    # Both admin and production staff see the same scope:
    # all logs made by admin or production users
    logs = ProductionLog.objects.select_related(
        'snack_item', 'logged_by'
    ).filter(
        logged_by__role__in=['admin', 'production']
    ).order_by('-production_date', '-created_at')

    logs = _date_range_filter(logs, 'production_date', f['date_from'], f['date_to'])

    if f['user_id']:
        logs = logs.filter(logged_by__id=f['user_id'])
    if f['item_id']:
        logs = logs.filter(snack_item__id=f['item_id'])

    # Stat calculations on filtered queryset
    total_entries = logs.count()
    total_qty = logs.aggregate(t=Sum('quantity'))['t'] or 0

    # Top produced item in this filter range
    top_item = (
        logs.values('snack_item__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
        .first()
    )

    # Unique staff who logged in this range
    unique_staff = logs.values('logged_by').distinct().count()

    # User dropdown — admin + production staff
    users = CustomUser.objects.filter(
        role__in=['admin', 'production'], is_deleted=False
    ).order_by('full_name')

    items = SnackItem.objects.order_by('name')

    return render(request, 'reports/production.html', {
        'logs': logs,
        'users': users,
        'items': items,
        'filters': f,
        'total_entries': total_entries,
        'total_qty': total_qty,
        'top_item': top_item,
        'unique_staff': unique_staff,
    })


@sales_required
def sales_report(request):
    f = _parse_filters(request, 'date_from', 'date_to', 'user_id', 'item_id')

    # Both admin and sales staff see the same scope:
    # all completed transactions made by admin or sales users
    transactions = SaleTransaction.objects.select_related(
        'sold_by'
    ).prefetch_related('items__snack_item').filter(
        status='completed',
        sold_by__role__in=['admin', 'sales'],
    ).order_by('-sale_date', '-created_at')

    transactions = _date_range_filter(transactions, 'sale_date', f['date_from'], f['date_to'])

    if f['user_id']:
        transactions = transactions.filter(sold_by__id=f['user_id'])
    if f['item_id']:
        transactions = transactions.filter(items__snack_item__id=f['item_id']).distinct()

    # Stat calculations
    total_transactions = transactions.count()
    grand_total = sum(t.total_amount for t in transactions)

    # Top selling item in range
    from apps.sales.models import SaleTransactionItem
    item_filter_kwargs = {}
    if f['date_from']:
        parsed = parse_date(f['date_from'])
        if parsed:
            item_filter_kwargs['transaction__sale_date__gte'] = parsed
    if f['date_to']:
        parsed = parse_date(f['date_to'])
        if parsed:
            item_filter_kwargs['transaction__sale_date__lte'] = parsed

    top_item = (
        SaleTransactionItem.objects.filter(
            transaction__status='completed',
            transaction__sold_by__role__in=['admin', 'sales'],
            **item_filter_kwargs,
        )
        .values('snack_item__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')
        .first()
    )

    # Unique staff who sold in this range
    unique_staff = transactions.values('sold_by').distinct().count()

    # User dropdown
    users = CustomUser.objects.filter(
        role__in=['admin', 'sales'], is_deleted=False
    ).order_by('full_name')

    items = SnackItem.objects.order_by('name')

    return render(request, 'reports/sales.html', {
        'transactions': transactions,
        'users': users,
        'items': items,
        'filters': f,
        'grand_total': grand_total,
        'total_transactions': total_transactions,
        'top_item': top_item,
        'unique_staff': unique_staff,
    })


@login_required
def waste_report(request):
    f = _parse_filters(request, 'date_from', 'date_to', 'user_id', 'status')

    reports = WasteReport.objects.select_related(
        'snack_item', 'reported_by', 'reviewed_by'
    ).order_by('-waste_date', '-created_at')

    reports = _date_range_filter(reports, 'waste_date', f['date_from'], f['date_to'])

    if f['user_id']:
        reports = reports.filter(reported_by__id=f['user_id'])
    if f['status']:
        reports = reports.filter(status=f['status'])

    # Role scoping — admin sees all, others see own department
    if request.user.role == 'production':
        reports = reports.filter(reported_by__role='production')
    elif request.user.role == 'sales':
        reports = reports.filter(reported_by__role='sales')

    # Stat counts on the already-filtered queryset
    total_count = reports.count()
    pending_count = reports.filter(status='pending').count()
    approved_count = reports.filter(status='approved').count()
    rejected_count = reports.filter(status='rejected').count()

    # User dropdown scoped by role
    if request.user.role == 'admin':
        users = CustomUser.objects.filter(
            is_deleted=False
        ).exclude(role='admin').order_by('full_name')
    else:
        users = CustomUser.objects.filter(
            role=request.user.role, is_deleted=False
        ).order_by('full_name')

    return render(request, 'reports/waste.html', {
        'reports': reports,
        'users': users,
        'filters': f,
        'total_count': total_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'status_choices': [
            ('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')
        ],
    })


@admin_required
def summary_report(request):
    f = _parse_filters(request, 'date_from', 'date_to')

    prod_qs = ProductionLog.objects.select_related(
        'snack_item', 'logged_by'
    ).filter(logged_by__role__in=['admin', 'production'])
    prod_qs = _date_range_filter(prod_qs, 'production_date', f['date_from'], f['date_to'])

    sale_qs = SaleTransaction.objects.filter(
        status='completed',
        sold_by__role__in=['admin', 'sales'],
    ).select_related('sold_by').prefetch_related('items__snack_item')
    sale_qs = _date_range_filter(sale_qs, 'sale_date', f['date_from'], f['date_to'])

    waste_qs = WasteReport.objects.select_related('snack_item', 'reported_by')
    waste_qs = _date_range_filter(waste_qs, 'waste_date', f['date_from'], f['date_to'])

    prod_total_qty = prod_qs.aggregate(t=Sum('quantity'))['t'] or 0
    sale_total_amount = sum(t.total_amount for t in sale_qs)
    sale_total_count = sale_qs.count()
    waste_total_qty = waste_qs.aggregate(t=Sum('quantity'))['t'] or 0
    waste_approved_qty = waste_qs.filter(status='approved').aggregate(t=Sum('quantity'))['t'] or 0
    waste_pending_count = waste_qs.filter(status='pending').count()

    return render(request, 'reports/summary.html', {
        'prod_logs': prod_qs.order_by('-production_date', '-created_at'),
        'sale_transactions': sale_qs.order_by('-sale_date', '-created_at'),
        'waste_reports': waste_qs.order_by('-waste_date', '-created_at'),
        'prod_total_qty': prod_total_qty,
        'sale_total_amount': sale_total_amount,
        'sale_total_count': sale_total_count,
        'waste_total_qty': waste_total_qty,
        'waste_approved_qty': waste_approved_qty,
        'waste_pending_count': waste_pending_count,
        'filters': f,
    })