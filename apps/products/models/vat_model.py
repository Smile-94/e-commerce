from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    DecimalField,
    Index,
    TextChoices,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from apps.common.functions.validator.numaric_validator import min_decimal_value
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)


# * <<-----------------------------*** VAT Type Choices ***----------------------------------->>
class VatTypeChoices(TextChoices):
    """
    VAT Type Choices
    """

    PERCENTAGE = "percentage", _("Percentage")
    FLAT_RATE = "flat_rate", _("Flat Rate")


# * <<-----------------------------------*** VAT Table ***------------------------------------->>
class Vat(DjangoBaseModel):
    """
    VAT Table
    """

    vat_amount = DecimalField(
        max_digits=19,
        decimal_places=4,
        default=Decimal("0.00"),
        blank=True,
        null=True,
        validators=[min_decimal_value],
        unique=True,
    )
    value_type = CharField(
        max_length=10,
        choices=VatTypeChoices.choices,
        default=VatTypeChoices.PERCENTAGE,
        blank=True,
        null=True,
    )
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "VAT"
        verbose_name_plural = "VAT"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["value_type"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "vat"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure vat_amount is unique.
        Raises a ValidationError if a vat with the same vat_amount already exists.
        """
        # Check if a vat with the same vat_amount already exists
        if Vat.objects.filter(vat_amount=self.vat_amount).exclude(id=self.id).exists():
            raise ValidationError(
                _("A VAT with the same amount already exists"),
            )

        super().clean()  # Call the parent's clean method

    # Save the instance after cleaning up
    def save(self, *args, **kwargs):
        """
        Call the clean method before saving the model instance.
        """
        self.full_clean()

        return super().save(*args, **kwargs)

    # Return a string representation of the model instance
    def __str__(self):
        """
        Returns the string representation of the model instance.
        :return: str: The string representation of the model instance.
        """
        return f"{self.vat_amount} {self.value_type}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<Vat: {self.vat_amount} {self.value_type}> <id: {self.id}"
