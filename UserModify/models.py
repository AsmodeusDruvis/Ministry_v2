from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Models Of The Abyss USERS




class UserVoid(AbstractUser):

    USER_ROLES = [
        ('Academy', 'Academy_member'),
        ('Minister', 'Team_member'),
    ]
    

    role = models.CharField(max_length=50, choices=USER_ROLES, default='Academy_member')

    email = models.EmailField(unique=True, max_length=255)  
    email_verified = models.BooleanField(default=False)  # New field for email verification
    verification_token = models.CharField(max_length=255, blank=True, null=True) 


    is_active = models.BooleanField(default=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)


    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    def __str__(self):
        return self.username  

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
