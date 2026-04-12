from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('add/', views.item_add, name='item_add'),
    path('<uuid:pk>/edit/', views.item_edit, name='item_edit'),
    path('<uuid:pk>/toggle-active/', views.item_toggle_active, name='item_toggle_active'),
    path('<uuid:pk>/delete/', views.item_delete, name='item_delete'),
]