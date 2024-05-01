from django.contrib import admin
from django.urls import path, include

import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("dashboard.urls")),
]
