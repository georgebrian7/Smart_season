from django.db import models
from django.contrib.auth.models import AbstractUser
 
class CustomUser(AbstractUser):
    """
    Custom User model with role-based authentication
    """
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('field_agent', 'Field Agent'),
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='field_agent',
        help_text="User role determines access permissions"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_field_agent(self):
        return self.role == 'field_agent'
 
# Create your models here.
