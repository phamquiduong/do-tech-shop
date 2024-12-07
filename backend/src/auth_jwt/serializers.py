from typing import Any, Dict

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from users.validators import validate_phone_number


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["phone_number"] = serializers.CharField(validators=[validate_phone_number], write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        return {
            "access_token": data["access"],
            "refresh_token": data["refresh"],
        }


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)
    refresh = None
    access = None

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        attrs["refresh"] = attrs["refresh_token"]
        data = super().validate(attrs)

        return {
            "access_token": data["access"],
            "refresh_token": data["refresh"],
        }
