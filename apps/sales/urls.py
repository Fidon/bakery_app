from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleHistoryView.as_view(), name='history'),
    path('new/', views.sale_new, name='new'),
    path('<uuid:pk>/detail/', views.SaleDetailView.as_view(), name='detail'),
    path('<uuid:pk>/cancel/', views.sale_cancel, name='cancel'),
    path('item/<uuid:pk>/price/', views.get_item_price, name='get_item_price'),
]