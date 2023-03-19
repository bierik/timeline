from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "full_name"]


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_validation = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["password"] != attrs["password_validation"]:
            raise serializers.ValidationError("Passwort stimmt nicht überein")
        return attrs
