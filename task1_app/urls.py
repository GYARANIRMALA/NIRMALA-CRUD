from rest_framework.routers import DefaultRouter
from django.urls import path, include
from task1_app.models import Blog, Comments
from task1_app.serializers import BlogSerializer, CommentsSerializer
from task1_app.views import BlogApi, CommentsApi


router = DefaultRouter()
router.register("blog", BlogApi, "Blog")
router.register(":id/comments", CommentsApi, "Comments")








urlpatterns = [
    path("", include(router.urls)),
]