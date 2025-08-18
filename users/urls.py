from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView,ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/profile/',ProfileView.as_view(),name='profile')
]
