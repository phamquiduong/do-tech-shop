import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from main.api_exceptions import ConflictError
from users.validators import validate_phone_number

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(min_length=10, max_length=12, validators=[validate_phone_number])
    password = serializers.CharField(write_only=True, validators=[validate_password])

    username = serializers.CharField(read_only=True)

    def to_internal_value(self, data):
        phone_number = re.sub(r"[^\+\d]", "", data["phone_number"])

        if phone_number.startswith("0"):
            phone_number = "+84" + phone_number[1:]

        data["phone_number"] = phone_number
        return super().to_internal_value(data)

    def create(self, validated_data):
        if UserModel.objects.filter(phone_number=validated_data["phone_number"]).first() is not None:
            raise ConflictError(detail="Phone number is already registered")

        user = UserModel.objects.create_user(
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )

        return user

    class Meta:
        model = UserModel
        fields = ("id", "phone_number", "username", "password")
