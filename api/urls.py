from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('drivers', views.DriverViewSet, basename='drivers')
router.register(
    'drivers-not-loaded', views.NotLoadedDriversViewSet,
    basename='not-loaded-drivers'
)
router.register('locations', views.LocationViewSet, basename='locations')

urlpatterns = [
    path('', include(router.urls)),
]
