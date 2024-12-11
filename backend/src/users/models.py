import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from users.validators import validate_phone_number


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, password: str, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")

        extra_fields.setdefault("username", str(uuid.uuid4()).replace("-", ""))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True
        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class User(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=15, validators=[validate_phone_number])
    is_verify_phone_number = models.BooleanField(default=False)
    is_verify_email = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"

    objects = UserManager()  # type: ignore

    class Meta:
        db_table = "users"
