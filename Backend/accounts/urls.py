from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Definições da conta
    path('settings/', views.settings_view, name='settings'),
    path('settings/profile/', views.update_profile, name='update_profile'),
    path('settings/avatar/remove/', views.remove_avatar, name='remove_avatar'),
    path('settings/password/', views.change_password, name='change_password'),
    path('settings/delete/', views.delete_account, name='delete_account'),
]
