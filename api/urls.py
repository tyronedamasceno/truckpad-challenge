from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('drivers', views.DriverViewSet, basename='drivers')

urlpatterns = [
    path('', include(router.urls)),
]
