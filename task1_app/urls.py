from rest_framework.routers import DefaultRouter
from django.urls import path, include
from task1_app.models import Blog, Comments
from task1_app.serializers import BlogSerializer, CommentsSerializer
from task1_app.views import BlogApi, CommentsApi, show_comment


router = DefaultRouter()
router.register("blog", BlogApi, "Blog")
router.register("comments", CommentsApi, "Comments")









urlpatterns = [
    path("", include(router.urls)),
    path('blog/:<str:id>/<str:comment>/', show_comment),  
]