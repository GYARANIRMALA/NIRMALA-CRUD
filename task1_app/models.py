from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                PermissionsMixin
import uuid


class Blog(models.Model):
    class StatusTypes(models.TextChoices):
        Draft = "Draft"
        Published = "Published"
        Pending = "Pending"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50,default="")
    description = models.CharField(max_length=150,default="")
    primary_image = models.CharField(max_length=150,default="")
    likes = models.IntegerField()
    views = models.IntegerField()
    
    status = models.CharField(max_length=50,default="",choices=StatusTypes.choices)
    active = models.BooleanField(default=True)
    order = models.IntegerField()

    created_by = models.CharField(max_length=50,default="")
    updated_by = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.id

class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=50,default="")

    blog_id = models.ForeignKey(Blog, related_name="blog_id", on_delete=models.CASCADE, null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    status = models.CharField(max_length=50,default="")
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    created_by = models.CharField(max_length=50,default="")
    updated_by = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class User(AbstractBaseUser, PermissionsMixin):

    class RoleTypes(models.TextChoices):
        admin = "admin"
        support = "support"
        user = "user"
    
    class StatusTypes(models.TextChoices):
        inactive = "inactive"
        active = "active"
        blocked = "blocked"

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, default="", unique=True)
    password = models.CharField(max_length=500, default="")		
    fullname = models.CharField(max_length=50)	
    role = models.CharField(max_length=50, choices=RoleTypes.choices,default="")		
		
    status = models.CharField(max_length=50, choices=StatusTypes.choices,default="")	
    active = models.BooleanField(default=True)
		
    created_by = models.CharField(max_length=50,default="")
    updated_by = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = BaseUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
	
            