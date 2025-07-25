from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # Login and logout at root
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),  # Fixed this line

    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('responder-dashboard/', views.responder_dashboard, name='responder_dashboard'),

    # Incident Management
    path('admin/incidents/create/', views.create_incident, name='create_incident'),
    path('admin/incident/<int:incident_id>/', views.manage_incident, name='manage_incident'),

    # User Management
    path('admin/users/create/', views.create_user, name='create_user'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path('responder/incident/<int:incident_id>/', views.responder_incident_detail, name='responder-incident-detail'),
    path('admin/incident/<int:incident_id>/progress/', views.admin_incident_progress, name='admin-incident-progress'),
]