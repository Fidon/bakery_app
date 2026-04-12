from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class ProductionRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in ('admin', 'production'):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


class SalesRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in ('admin', 'sales'):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)


# ── Function-based decorators ──

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def production_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ('admin', 'production'):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def sales_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ('admin', 'sales'):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper