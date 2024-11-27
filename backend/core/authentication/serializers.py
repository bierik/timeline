from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "full_name"]


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)
    password_validation = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["password"] != attrs["password_validation"]:
            raise serializers.ValidationError("Passwort stimmt nicht überein")
        return attrs


class AuthSerializer(serializers.Serializer):
    """serializer for the user authentication object"""

    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=username, password=password)

        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs
