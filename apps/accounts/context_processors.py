from apps.waste.models import WasteReport

def bakery_context(request):
    pending_waste_count = 0
    if request.user.is_authenticated and request.user.role == 'admin':
        pending_waste_count = WasteReport.objects.filter(status='pending').count()
    return {'pending_waste_count': pending_waste_count}