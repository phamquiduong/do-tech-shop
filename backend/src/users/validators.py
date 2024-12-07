import re

from django.core.exceptions import ValidationError

from users.constants import PHONE_NUMBER_REGEX


def validate_phone_number(phone_number: str) -> None:
    if not re.match(PHONE_NUMBER_REGEX, phone_number):
        raise ValidationError('Phone number from Viet Nam must be a +84xxxxxxxxx')
