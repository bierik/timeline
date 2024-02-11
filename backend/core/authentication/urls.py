from core.authentication.views import ChangePasswordView
from core.authentication.views import LoginView
from core.authentication.views import UserView
from django.urls import path
from knox import views as knox_views


urlpatterns = [
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("user/", UserView.as_view(), name="user"),
    path("login/", LoginView.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]
