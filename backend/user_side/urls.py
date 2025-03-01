from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViewSet

router = DefaultRouter()
router.register(r'loans', ViewSet)  # Register ViewSet

urlpatterns = [
    path('api/', include(router.urls)),  # Include all generated routes
]
