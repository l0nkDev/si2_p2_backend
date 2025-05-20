from django.urls import include, path
from rest_framework import routers
from server.backend import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include('server.backend.urls'))
]