from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum, Count

from .forms import UserAddForm, UserEditForm, ProfileEditForm, ChangePasswordForm, SetNewPasswordForm
from .mixins import admin_required

User = get_user_model()


# ── Auth ──────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return JsonResponse({'success': False, 'error': 'Your account has been deactivated. Contact the administrator.'})
            if user.is_deleted:
                return JsonResponse({'success': False, 'error': 'Account not found.'})
            login(request, user)
            if user.must_change_password:
                return JsonResponse({'success': True, 'redirect': reverse('accounts:set_new_password')})
            next_url = request.POST.get('next') or request.GET.get('next') or reverse('accounts:dashboard')
            return JsonResponse({'success': True, 'redirect': next_url})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def set_new_password(request):
    """Force password change on first login."""
    if not request.user.must_change_password:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.must_change_password = False
            request.user.save(update_fields=['password', 'must_change_password'])
            update_session_auth_hash(request, request.user)
            return JsonResponse({'success': True, 'redirect': reverse('accounts:dashboard')})
        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'accounts/set_new_password.html')


# ── Dashboard ─────────────────────────────────────────
@login_required
def dashboard(request):
    from django.shortcuts import render
    user = request.user
    today = timezone.localdate()
    context = {'today': today}

    if user.role == 'admin':
        from apps.production.models import ProductionLog
        from apps.sales.models import SaleTransaction
        from apps.waste.models import WasteReport
        from apps.inventory.models import SnackItem

        # Today's production — total units logged today
        production_today = ProductionLog.objects.filter(
            production_date=today
        ).aggregate(total=Sum('quantity'))['total'] or 0

        # Today's sales — total amount and transaction count
        sales_today = SaleTransaction.objects.filter(
            sale_date=today,
            status='completed'
        ).aggregate(
            total_amount=Sum('total_amount'),
            count=Count('id')
        )
        sales_amount_today = sales_today['total_amount'] or 0
        sales_count_today  = sales_today['count'] or 0

        # Pending waste approvals
        pending_waste = WasteReport.objects.filter(status='pending').count()

        # Active snack items
        active_items = SnackItem.objects.filter(is_active=True).count()

        # Recent transactions (last 5)
        recent_sales = SaleTransaction.objects.select_related(
            'sold_by'
        ).order_by('-created_at')[:5]

        # Recent production logs (last 5)
        recent_production = ProductionLog.objects.select_related(
            'snack_item', 'logged_by'
        ).order_by('-created_at')[:5]

        context.update({
            'production_today': production_today,
            'sales_amount_today': sales_amount_today,
            'sales_count_today': sales_count_today,
            'pending_waste': pending_waste,
            'active_items': active_items,
            'recent_sales': recent_sales,
            'recent_production': recent_production,
        })

    elif user.role == 'production':
        from apps.production.models import ProductionLog
        from apps.inventory.models import SnackItem

        # Today's production by this user
        my_today_logs = ProductionLog.objects.filter(
            logged_by=user,
            production_date=today
        ).select_related('snack_item')

        my_today_total = my_today_logs.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        # This user's total production this month
        month_total = ProductionLog.objects.filter(
            logged_by=user,
            production_date__year=today.year,
            production_date__month=today.month,
        ).aggregate(total=Sum('quantity'))['total'] or 0

        # Available items to produce
        active_items = SnackItem.objects.filter(
            is_active=True
        ).order_by('name')

        context.update({
            'my_today_logs': my_today_logs,
            'my_today_total': my_today_total,
            'month_total': month_total,
            'active_items': active_items,
        })

    elif user.role == 'sales':
        from apps.sales.models import SaleTransaction, SaleTransactionItem
        from apps.inventory.models import SnackItem

        # Today's sales by this user
        my_today_sales = SaleTransaction.objects.filter(
            sold_by=user,
            sale_date=today,
            status='completed'
        ).aggregate(
            total_amount=Sum('total_amount'),
            count=Count('id')
        )
        my_sales_amount_today = my_today_sales['total_amount'] or 0
        my_sales_count_today  = my_today_sales['count'] or 0

        # This month's total
        month_total = SaleTransaction.objects.filter(
            sold_by=user,
            sale_date__year=today.year,
            sale_date__month=today.month,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        # Top selling item this month by this user
        top_item = SaleTransactionItem.objects.filter(
            transaction__sold_by=user,
            transaction__sale_date__year=today.year,
            transaction__sale_date__month=today.month,
            transaction__status='completed'
        ).values(
            'snack_item__name'
        ).annotate(
            total_qty=Sum('quantity')
        ).order_by('-total_qty').first()

        # Recent transactions by this user (last 5)
        recent_sales = SaleTransaction.objects.filter(
            sold_by=user
        ).order_by('-created_at')[:5]

        # Available items with stock
        available_items = SnackItem.objects.filter(
            is_active=True,
            current_stock__gt=0
        ).count()

        context.update({
            'my_sales_amount_today': my_sales_amount_today,
            'my_sales_count_today': my_sales_count_today,
            'month_total': month_total,
            'top_item': top_item,
            'recent_sales': recent_sales,
            'available_items': available_items,
        })

    return render(request, 'accounts/dashboard.html', context)


# ── Profile ───────────────────────────────────────────
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user, user_role=request.user.role)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return JsonResponse({'success': True, 'message': 'Password changed successfully.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})


# ── User management (admin only) ──────────────────────
@admin_required
def user_list(request):
    users = User.objects.filter(is_deleted=False).exclude(pk=request.user.pk).order_by('full_name')
    return render(request, 'accounts/user_list.html', {'users': users})


@admin_required
def user_add(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({'success': True, 'message': f'User "{user.full_name}" created. Default password is their username in caps.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})


@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': f'User "{user.full_name}" updated successfully.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})


@admin_required
def user_toggle_active(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'})
    user = get_object_or_404(User, pk=pk, is_deleted=False)
    if user == request.user:
        return JsonResponse({'success': False, 'error': 'You cannot deactivate your own account.'})
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    status = 'deactivated' if not user.is_active else 'activated'
    return JsonResponse({
        'success': True,
        'message': f'User "{user.full_name}" has been {status}.',
        'is_active': user.is_active
    })


@admin_required
def user_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'})
    user = get_object_or_404(User, pk=pk, is_deleted=False)
    if user == request.user:
        return JsonResponse({'success': False, 'error': 'You cannot delete your own account.'})
    user.is_deleted = True
    user.is_active = False
    user.save(update_fields=['is_deleted', 'is_active'])
    return JsonResponse({'success': True, 'message': f'User "{user.full_name}" has been removed.'})


@admin_required
def user_reset_password(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'})
    user = get_object_or_404(User, pk=pk, is_deleted=False)
    # Reset to username in capital letters
    user.set_password(user.username.upper())
    user.must_change_password = True
    user.save(update_fields=['password', 'must_change_password'])
    return JsonResponse({'success': True, 'message': f'Password for "{user.full_name}" reset to their username in caps.'})
