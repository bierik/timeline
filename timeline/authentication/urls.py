from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from timeline.authentication.views import ChangePasswordView, LogoutView, UserView

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("user/", UserView.as_view(), name="user"),
]
