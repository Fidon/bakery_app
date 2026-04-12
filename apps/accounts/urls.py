from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('change-password/', views.change_password, name='change_password'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<uuid:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<uuid:pk>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),
    path('users/<uuid:pk>/reset-password/', views.user_reset_password, name='user_reset_password'),
    path('users/<uuid:pk>/delete/', views.user_delete, name='user_delete'),
]