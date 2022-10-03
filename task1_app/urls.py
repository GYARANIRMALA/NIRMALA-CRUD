from rest_framework.routers import DefaultRouter
from django.urls import path, include
from task1_app.models import Blog, Comments, User
from task1_app.serializers import BlogSerializer, CommentsSerializer, UserSerializer
from task1_app.views import BlogApi, CommentsApi, show_comment, UserApi, LoginView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register("blogs", BlogApi, "Blog")
router.register("comments", CommentsApi, "Comments")
router.register("user", UserApi, "User")
# router.register("login", LoginApi, "Login")



urlpatterns = [
    path("", include(router.urls)),
    path('blog/<str:id>/comments/', show_comment),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view()),
]