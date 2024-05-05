from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.login_view,name="signin"),
    path('signup',views.signup_view,name="signup"),
    path('logout',views.userlogout,name="logout"),
    
    
]