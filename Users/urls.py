from django.urls import path
from . import views

urlpatterns = [
    path("signin", views.signinpage, name="SignIn"),
    path("signout",views.signout, name="SignOut"),
    path("login",views.userlogin),
    
]
