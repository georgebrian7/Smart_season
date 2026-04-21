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
    
    return render(request, 'auth/login.html', {'form': form})
 
 
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
    
    return render(request, 'auth/register.html', {'form': form})
 
 
def logout_view(request):
    """
    Function-based logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('auth:login')
 
 