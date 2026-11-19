from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('field_agent', 'Field Agent'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='field_agent',
        db_index=True,
        help_text='User role determines access permissions',
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['date_joined'], name='custom_user_joined_idx'),
            models.Index(fields=['last_login'], name='custom_user_login_idx'),
        ]

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    def is_admin(self):
        return self.role == 'admin'

    def is_field_agent(self):
        return self.role == 'field_agent'
