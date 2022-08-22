from django.db import models
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
    likes = models.IntegerField(blank=True,null=True)
    dislike = models.IntegerField(blank=True,null=True)

    status = models.CharField(max_length=50,default="")
    active = models.BooleanField(default=True)
    order = models.IntegerField(blank=True,null=True)

    created_by = models.CharField(max_length=50,default="")
    updated_by = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment