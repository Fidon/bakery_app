from django.urls import path
from apps.reports import views

app_name = 'reports'

urlpatterns = [
    path('production/', views.production_report, name='production'),
    path('sales/', views.sales_report, name='sales'),
    path('waste/', views.waste_report, name='waste'),
    path('summary/', views.summary_report, name='summary'),
]