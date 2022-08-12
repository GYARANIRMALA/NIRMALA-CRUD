from django.db import models
import uuid

class Blog(models.Model):
    class StatusTypes(models.TextChoices):
        draft = "draft"
        published = "published"
        pending = "pending"

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
    

    def __str__(name):
        return self.name
