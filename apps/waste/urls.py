from django.urls import path
from apps.waste import views

app_name = 'waste'

urlpatterns = [
    path('report/', views.report_view,  name='report'),
    path('history/', views.history_view, name='history'),
    path('pending/', views.pending_view, name='pending'),
    path('<uuid:pk>/review/', views.review_view,  name='review'),
]