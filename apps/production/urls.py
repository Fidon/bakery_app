from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('log/', views.production_log_view, name='log'),
    path('history/', views.ProductionHistoryView.as_view(), name='history'),
    path('<uuid:pk>/delete/', views.production_delete, name='delete'),
]