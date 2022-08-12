from rest_framework.routers import DefaultRouter
from django.urls import path, include
from task1_app.models import Blog
from task1_app.serializers import BlogSerializer
from task1_app.views import BlogApi


router = DefaultRouter()
router.register("blog", BlogApi, "Blog")







urlpatterns = [
    path("", include(router.urls)),
]