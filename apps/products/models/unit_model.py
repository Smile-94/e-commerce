from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    Index,
    TextField,
    UniqueConstraint,
)

from apps.common.functions.validator.name_validator import validate_special_character
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)


# * <<-------------------------------------*** Product Unit Model ***-------------------------------------->>
class UnitAttribute(DjangoBaseModel):
    """
    Product Unit Attribute Model
    """

    attribute_name = CharField(max_length=255, unique=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Product Unit Attribute"
        verbose_name_plural = "Product Unit Attribute"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["attribute_name"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "product_unit_attribute"

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
                {
                    "attribute_name": "An attribute with this name already exists.",
                },
            )

        # Check any special character exist in the attribute_name
        if self.attribute_name:
            validate_special_character(
                self.attribute_name, field_name="attribute_name"
            )  # Validate attribute_name for special characters
        else:
            raise ValidationError(
                {
                    "attribute_name": "Attribute name cannot be empty.",
                },
            )

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
        return f"{self.attribute_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<ProductUnitAttribute: {self.attribute_name}> <id: {self.id}"


# * <<---------------------------------------------*** Product Unit Attribute Value ***-------------------->>
class UnitAttributeValue(DjangoBaseModel):
    """
    Product Unit Attribute Value Model
    """

    unit_attribute = ForeignKey(
        UnitAttribute, on_delete=CASCADE, related_name="unit_attributes"
    )
    unit_value = CharField(max_length=255)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Product Unit Value"
        verbose_name_plural = "Product Unit Value"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["unit_value"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "product_unit_value"
        constraints = [
            UniqueConstraint(
                fields=["unit_attribute", "unit_value"],
                name="unique_unit_value",
            ),
        ]

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure attribute_value is unique for a given unit_attribute.
        Raises a ValidationError if a value with the same name already exists for the same unit_attribute.
        """

        # Check any special character exist in the attribute_value
        if self.unit_value:
            validate_special_character(
                self.unit_value, field_name="unit_value"
            )  # Validate attribute_value for special characters
        else:
            raise ValidationError(
                {
                    "unit_value": "Attribute value cannot be empty.",
                },
            )

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
        return f"{self.unit_value}-({self.unit_attribute.attribute_name})"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<UnitAttributeValue: {self.unit_value}> <id: {self.id}"
