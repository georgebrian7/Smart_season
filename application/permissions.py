from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse_lazy

# ==================== DECORATORS ====================

def admin_required(view_func):
    """
    Decorator to require admin role for a view
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            raise PermissionDenied("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def field_agent_required(view_func):
    """
    Decorator to require field agent role for a view
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_field_agent():
            raise PermissionDenied("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_or_field_agent_required(view_func):
    """
    Decorator to require either admin or field agent role
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_admin() or request.user.is_field_agent()):
            raise PermissionDenied("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


# ==================== CLASS-BASED MIXINS ====================

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict view access to admin users only
    """
    login_url = 'login'
    permission_denied_message = "You must be an administrator to access this page."
    
    def test_func(self):
        return self.request.user.is_admin()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.permission_denied_message)
        return redirect(self.login_url)


class FieldAgentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict view access to field agent users only
    """
    login_url = 'login'
    permission_denied_message = "You must be a field agent to access this page."
    
    def test_func(self):
        return self.request.user.is_field_agent()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.permission_denied_message)
        return redirect(self.login_url)


class AdminOrFieldAgentMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict view access to authenticated users (admin or field agent)
    """
    login_url = 'login'
    permission_denied_message = "You do not have permission to access this page."
    
    def test_func(self):
        return self.request.user.is_admin() or self.request.user.is_field_agent()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.permission_denied_message)
        return redirect(self.login_url)