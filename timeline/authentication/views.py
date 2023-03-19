from rest_framework.response import Response
from rest_framework.views import APIView

from timeline.authentication.serializers import PasswordResetSerializer, UserSerializer


class LogoutView(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response()


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
