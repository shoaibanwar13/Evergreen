from django.urls import path, include
from Api import views

urlpatterns = [
    path('v1/auth/', include('Authentication.urls.v1.urls')),
]