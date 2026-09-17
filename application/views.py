from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import CustomUser
from .permissions import admin_required, field_agent_required, admin_or_field_agent_required
 
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_view(request):
    """
    Function-based login view
    """
    if request.user.is_authenticated:
        if request.user.is_admin():
            return redirect('auth:admin_dashboard')
        elif request.user.is_field_agent():
            return redirect('auth:field_agent_dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on role
            if user.is_admin():
                return redirect('auth:admin_dashboard')
            elif user.is_field_agent():
                return redirect('auth:field_agent_dashboard')
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'Auth login.html', {'form': form})
 
 
def register_view(request):
    """
    Function-based registration view
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Account created successfully! Please log in.'
            )
            return redirect('auth:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'Auth register.html', {'form': form})
 
 
def logout_view(request):
    """
    Function-based logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('auth:login')
 
@admin_required
def admin_dashboard_view(request):
    """
    Admin dashboard - only accessible to admins
    """
    context = {
        'total_users': CustomUser.objects.count(),
        'field_agents': CustomUser.objects.filter(role='field_agent').count(),
        'admins': CustomUser.objects.filter(role='admin').count(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
 
 
@field_agent_required
def field_agent_dashboard_view(request):
    """
    Field agent dashboard - only accessible to field agents
    """
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard/field_agent_dashboard.html', context)
 
 
# ==================== PROFILE VIEWS ====================
 
@login_required(login_url='auth:login')
def profile_view(request):
    """
    User profile view - accessible to all authenticated users
    """
    context = {
        'user': request.user,
    }
    return render(request, 'auth/profile.html', context)
 
 
@login_required(login_url='auth:login')
def edit_profile_view(request):
    """
    Edit user profile
    """
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('auth:profile')
    
    context = {
        'user': request.user,
    }
    return render(request, 'auth/edit_profile.html', context)
 
 
# ==================== ADMIN USER MANAGEMENT VIEWS ====================
 
@admin_required
def manage_users_view(request):
    """
    Admin view to manage all users
    """
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Filter by role if specified
    role = request.GET.get('role')
    if role:
        users = users.filter(role=role)
    
    # Filter by active status if specified
    status = request.GET.get('status')
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
    
    context = {
        'users': users,
        'total_users': CustomUser.objects.count(),
        'field_agents': CustomUser.objects.filter(role='field_agent').count(),
        'admins': CustomUser.objects.filter(role='admin').count(),
    }
    return render(request, 'admin/manage_users.html', context)
 
 
@admin_required
def user_detail_view(request, pk):
    """
    Admin view to see detailed user information
    """
    try:
        user = CustomUser.objects.get(pk=pk)
        context = {
            'detail_user': user,
        }
        return render(request, 'admin/user_detail.html', context)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('auth:manage_users')
 
 
@admin_required
def deactivate_user_view(request, pk):
    """
    Admin action to deactivate a user
    """
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(pk=pk)
            user.is_active = False
            user.save()
            messages.success(request, f"User {user.username} has been deactivated.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    
    return redirect('auth:manage_users')
 
 
@admin_required
def activate_user_view(request, pk):
    """
    Admin action to activate a user
    """
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(pk=pk)
            user.is_active = True
            user.save()
            messages.success(request, f"User {user.username} has been activated.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    
    return redirect('auth:manage_users')
 
 
@admin_required
def delete_user_view(request, pk):
    """
    Admin action to delete a user
    """
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(pk=pk)
            username = user.username
            user.delete()
            messages.success(request, f"User {username} has been deleted.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    
    return redirect('auth:manage_users')
 
 
@admin_required
def change_user_role_view(request, pk):
    """
    Admin action to change user role
    """
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(pk=pk)
            new_role = request.POST.get('role')
            
            if new_role in ['admin', 'field_agent']:
                user.role = new_role
                user.is_staff = (new_role == 'admin')
                user.save()
                messages.success(request, f"User role changed to {user.get_role_display()}.")
            else:
                messages.error(request, "Invalid role.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    
    return redirect('auth:manage_users')
 
 
# ==================== FIELD AGENT SPECIFIC VIEWS ====================
 
@field_agent_required
def field_agent_tasks_view(request):
    """
    Field agent view for their assigned tasks
    """
    context = {
        'user': request.user,
    }
    return render(request, 'field_agent/tasks.html', context)
 
 
@field_agent_required
def field_agent_reports_view(request):
    """
    Field agent view to submit reports
    """
    if request.method == 'POST':
        # Handle report submission
        messages.success(request, 'Report submitted successfully.')
        return redirect('auth:field_agent_reports')
    
    context = {
        'user': request.user,
    }
    return render(request, 'field_agent/reports.html', context)
 
 
# ==================== SEARCH & LIST VIEWS ====================
 
@admin_required
def search_users_view(request):
    """
    Admin view to search users
    """
    query = request.GET.get('q', '')
    users = CustomUser.objects.all()
    
    if query:
        users = users.filter(
            username__icontains=query
        ) | users.filter(
            email__icontains=query
        ) | users.filter(
            first_name__icontains=query
        ) | users.filter(
            last_name__icontains=query
        )
    
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'admin/search_users.html', context)
 
 
@admin_required
def user_activity_log_view(request):
    """
    Admin view to see user activity logs
    """
    users = CustomUser.objects.all().order_by('-last_login')
    
    context = {
        'users': users,
    }
    return render(request, 'admin/activity_log.html', context)
 
 
# ==================== EXPORT VIEWS ====================
 
@admin_required
def export_users_view(request):
    """
    Admin view to export users as CSV
    """
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Role', 'Active', 'Date Joined'])
    
    for user in CustomUser.objects.all():
        writer.writerow([
            user.username,
            user.email,
            user.get_role_display(),
            'Yes' if user.is_active else 'No',
            user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        ])
    
    return response
 