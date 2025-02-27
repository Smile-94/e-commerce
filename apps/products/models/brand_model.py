from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    EmailField,
    ImageField,
    Index,
    TextField,
    URLField,
)
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.functions.validator.image_validator import (
    get_validate_image_extensions,
)
from apps.common.functions.validator.name_validator import validate_special_character
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)


# * <<--------------------------------------*** Product Brand Table ***--------------------------------------->>
class Brand(DjangoBaseModel):
    """
    Product Brand Table
    """

    brand_name = CharField(max_length=255, unique=True)
    origin_country = CharField(
        max_length=100, default="Bangladesh", blank=True, null=True
    )
    brand_logo = ImageField(upload_to="product/brands", blank=True, null=True)
    web_url = URLField(blank=True, null=True)
    contact_number = PhoneNumberField(blank=True, null=True)
    brand_email = EmailField(max_length=255, blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brand"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["brand_name"]),
            Index(fields=["origin_country"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "brand"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure brand_name is unique.
        Raises a ValidationError if a brand with the same name already exists.
        """
        # Check if a brand with the same name already exists
        if (
            self.__class__.objects.filter(brand_name__iexact=self.brand_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                _(
                    "A brand with this name already exists.",
                )
            )

        # Check any special character exist in the brand name
        if self.brand_name:
            validate_special_character(
                self.brand_name, field_name="brand_name"
            )  # Validate brand_name for special characters
        else:
            raise ValidationError(
                _(
                    "Brand name cannot be empty.",
                )
            )

        # Ensure brand_logo is a valid image file
        if self.brand_logo:
            get_validate_image_extensions(
                images=[
                    self.brand_logo,
                ],
                valid_extensions={".jpg", ".jpeg", ".png", ".webp"},
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
        return f"{self.brand_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<Brand: {self.brand_name}> <id: {self.id}"
