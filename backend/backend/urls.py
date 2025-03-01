"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import CustomAdminTokenObtainPairView,CustomUserTokenObtainPairView
from user_side.views import ViewSet  # Import your view
router = DefaultRouter()
router.register(r'loans', ViewSet)  # This creates /api/loans/
urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/user/login/", CustomUserTokenObtainPairView.as_view(), name="user_login"),
    path("api/admin/login/", CustomAdminTokenObtainPairView.as_view(), name="admin_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/",include("bank_auth.urls")),
    path('api/', include(router.urls)),  # This includes the loans API
    path('api/',include('admin_side.urls'))
]
