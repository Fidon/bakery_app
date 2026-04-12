from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls', namespace='accounts')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('production/', include('apps.production.urls', namespace='production')),
    path('sales/', include('apps.sales.urls', namespace='sales')),
    path('waste/', include('apps.waste.urls', namespace='waste')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)