from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    Index,
    TextField,
    UniqueConstraint,
)
from django.utils.translation import gettext_lazy as _

from apps.common.functions.validator.name_validator import (
    validate_special_character,
)
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)


# * <<--------------------------------------*** Variation Attribute Table ***--------------------------------------->>
class VariationAttribute(DjangoBaseModel):
    """
    Variation Attribute Table
    """

    attribute_name = CharField(max_length=255, unique=True)
    description = TextField(blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Variation Attribute"
        verbose_name_plural = "Variation Attribute"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["attribute_name"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "variation_attribute"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure attribute_name is unique.
        Raises a ValidationError if an attribute with the same name already exists.
        """
        # Check if an attribute with the same name already exists
        if (
            self.__class__.objects.filter(attribute_name__iexact=self.attribute_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                _("An attribute with this name already exists."),
            )
        # Check any special character exist in the attribute_name
        if self.attribute_name:
            validate_special_character(
                self.attribute_name
            )  # Validate attribute_name for special characters
        else:
            raise ValidationError(
                _("Attribute name is required."),
            )
        super().clean()  # Call the parent's clean method

    # Save the instance after cleaning up
    def save(self, *args, **kwargs):
        """
        Call the clean method before saving the model instance.
        """
        self.full_clean()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attribute_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<VariationAttribute: {self.attribute_name}>"


# * <<--------------------------------------*** Variation Attribute Value Table ***--------------------------------------->>
class VariationAttributeValue(DjangoBaseModel):
    """
    Variation Attribute Value Table
    """

    variation_attribute = ForeignKey(
        VariationAttribute,
        related_name="variation_attribute_value",
        on_delete=CASCADE,
        blank=True,
        null=True,
    )
    attribute_value = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Variation Attribute Value"
        verbose_name_plural = "Variation Attribute Values"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["attribute_value"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "variation_attribute_value"
        constraints = [
            UniqueConstraint(
                fields=["variation_attribute", "attribute_value"],
                name="unique_attribute_value",
            ),
        ]

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure attribute_value is unique for a given variation_attribute.
        Raises a ValidationError if a value with the same name already exists for the same variation_attribute.
        """
        # Check if a value with the same name already exists for the same variation_attribute
        if (
            self.__class__.objects.filter(
                variation_attribute_id=self.variation_attribute_id,
                attribute_value__iexact=self.attribute_value,
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                _(
                    "A value with this name already exists for the selected variation attribute."
                ),
            )
        # Check any special character exist in the attribute_value
        if self.attribute_value:
            validate_special_character(
                self.attribute_value
            )  # Validate attribute_value for special characters
        else:
            raise ValidationError(
                _("Attribute value is required."),
            )
        super().clean()  # Call the parent's clean method

    # Save the instance after cleaning up
    def save(self, *args, **kwargs):
        """
        Call the clean method before saving the model instance.
        """
        self.full_clean()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attribute_value}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<VariationAttributeValue: {self.attribute_value}>"
