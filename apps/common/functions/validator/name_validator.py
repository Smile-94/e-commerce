import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_special_character(field_value: str, field_name: str) -> any:
    """
    Validate the attribute name for special characters.
    """
    pattern = r"[@#$%&]"

    if re.search(pattern, field_value):
        raise ValidationError(
            _(f"{field_name} name cannot contain the following characters: @ # $ % &"),
        )
