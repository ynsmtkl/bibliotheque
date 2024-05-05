from django.contrib import admin
from django.urls import path, include

import dashboard

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include("dashboard.urls")),
    path('', include("livres.urls")),
    path('', include("login.urls")),
    path('', include("prets.urls")),
]
