"""Urls users."""

# Django
from django.urls import path
#from django.contrib.auth.views import LogoutView

# View
from users import views

urlpatterns = [
        # Management
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name="logout"
    ),
    path(
        route='me/profile/',
        view=views.ProfileDetailView.as_view(),
        name='profile'

    ),
    #path('register/', register_user, name="register"),
    #path("logout/", LogoutView.as_view(), name="logout")
]
