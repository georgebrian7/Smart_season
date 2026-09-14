"""
URL configuration for smartseason project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('field-agent/dashboard/', views.field_agent_dashboard_view, name='field_agent_dashboard'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Admin User Management
    path('admin/users/', views.manage_users_view, name='manage_users'),
    path('admin/users/<int:pk>/', views.user_detail_view, name='user_detail'),
    
    # Field Agent
    path('field-agent/tasks/', views.field_agent_tasks_view, name='field_agent_tasks'),
    path('field-agent/reports/', views.field_agent_reports_view, name='field_agent_reports'),
]
