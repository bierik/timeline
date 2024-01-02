from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from timeline.authentication.serializers import AuthSerializer
from timeline.authentication.serializers import PasswordResetSerializer
from timeline.authentication.serializers import UserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super().post(request, format=None)


class UserView(APIView):
    def get(self, request):
        user = UserSerializer(request.user).data
        return Response(data={"user": user})


class ChangePasswordView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["password"])
        request.user.save()
        return Response(status=204)
