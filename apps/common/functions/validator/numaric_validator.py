from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.translation import (
    gettext_lazy as _,
)


def min_decimal_value(value: Decimal, min_value: Decimal):
    """
    Validates that the given value is greater than or equal to the provided minimum value.

    Args:
        value (Decimal): The value to be validated.
        min_value (Decimal): The minimum allowed value.

    Raises:
        ValidationError: If the value is less than the minimum value.
    """

    if value < min_value:
        raise ValidationError(
            _("Value must be greater than or equal to {min_value}"),
            params={"value": value, "min_value": min_value},
        )
    elif value < 0.0:
        raise ValidationError(
            _("Value can not be negative number"),
            params={"value": value},
        )


def decimal_value_range(
    value: Decimal,
    min_value: Decimal,
    max_value: Decimal,
    *args,
    **kwargs,
) -> None:
    """
    Validates whether a Decimal value falls within a specified range.

    Args:
        value (Decimal): The Decimal value to validate.
        min_value (Decimal): The minimum allowed value (inclusive).
        max_value (Decimal): The maximum allowed value (inclusive).
        *args: Additional positional arguments (ignored).
        **kwargs: Additional keyword arguments (ignored).

    Raises:
        ValueError: If `min_value` is greater than `max_value` or if the value is outside the range.
    """
    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")

    if not (min_value <= value <= max_value):
        raise ValueError(
            f"Value {value} is outside the allowed range [{min_value}, {max_value}]"
        )
