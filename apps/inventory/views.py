from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import SnackItem
from .forms import SnackItemForm



class ItemListView(LoginRequiredMixin, ListView):
    model = SnackItem
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return SnackItem.objects.select_related('created_by').order_by('-created_at')


@login_required
def item_add(request):
    # Admin and Production may add items
    if request.user.role not in ('admin', 'production'):
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=405)

    form = SnackItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.created_by = request.user
        item.save()
        return JsonResponse({
            'success': True,
            'message': f'"{item.name}" has been added successfully.',
            'item': {
                'id': str(item.pk),
                'name': item.name,
                'unit': item.get_unit_display(),
                'price': str(item.price),
                'current_stock': item.current_stock,
                'is_active': item.is_active,
                'created_by': item.created_by.full_name,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
def item_edit(request, pk):
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    item = get_object_or_404(SnackItem, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=405)

    form = SnackItemForm(request.POST, instance=item)
    if form.is_valid():
        item = form.save()
        return JsonResponse({
            'success': True,
            'message': f'"{item.name}" has been updated successfully.',
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
def item_toggle_active(request, pk):
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    item = get_object_or_404(SnackItem, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=405)

    item.is_active = not item.is_active
    item.save(update_fields=['is_active'])
    status_label = 'activated' if item.is_active else 'deactivated'
    return JsonResponse({
        'success': True,
        'message': f'"{item.name}" has been {status_label}.',
        'is_active': item.is_active,
    })


@login_required
def item_delete(request, pk):
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    item = get_object_or_404(SnackItem, pk=pk)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=405)

    # Guard: do not delete if production logs or sales exist against this item
    if item.production_logs.exists() or item.sale_items.exists():
        return JsonResponse({
            'success': False,
            'error': 'Cannot delete this item — it has production or sales records attached. Deactivate it instead.'
        }, status=400)

    name = item.name
    item.delete()
    return JsonResponse({'success': True, 'message': f'"{name}" has been deleted.'})