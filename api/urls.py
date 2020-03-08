from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('drivers', views.DriverViewSet, basename='drivers')
router.register(
    'drivers-not-loaded', views.NotLoadedDriversViewSet,
    basename='not-loaded-drivers'
)
router.register(
    'drivers-with-own-vehicle', views.OwnVehicleDriversViewSet,
    basename='own-vehicle-drivers'
)
router.register('locations', views.LocationViewSet, basename='locations')
router.register(
    'origin-and-destiny', views.OriginAndDestinyViewSet,
    basename='origin-and-destiny'
)

urlpatterns = [
    path('', include(router.urls)),
]
