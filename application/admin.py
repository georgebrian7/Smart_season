from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
 
 
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for CustomUser model
    """
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'password'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone'),
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone'),
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Override save to ensure proper role assignment
        """
        if not change:  # New user
            obj.is_staff = obj.role == 'admin'
        super().save_model(request, obj, form, change)
 

