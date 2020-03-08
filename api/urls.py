from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views

driver_router = DefaultRouter()
driver_router.register('drivers', views.DriverViewSet, basename='drivers')
driver_router.register(
    'not-loaded', views.NotLoadedDriversViewSet,
    basename='not-loaded-drivers'
)
driver_router.register(
    'own-vehicle', views.OwnVehicleDriversViewSet,
    basename='own-vehicle-drivers'
)

location_router = DefaultRouter()
location_router.register(
    'locations', views.LocationViewSet, basename='locations'
)
location_router.register(
    'origin-and-destiny', views.OriginAndDestinyViewSet,
    basename='origin-and-destiny'
)

urlpatterns = [
    path('driver/', include(driver_router.urls)),
    path('location/', include(location_router.urls)),
    path(
        'driver/counter/<slug:period>/', views.DriversCounterView.as_view(),
        name='drivers-counter'
    )
]
