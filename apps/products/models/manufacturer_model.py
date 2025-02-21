from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    EmailField,
    ImageField,
    Index,
    ManyToManyField,
    TextChoices,
    TextField,
)
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.functions.validator.image_validator import (
    get_validate_image_extensions,
)
from apps.common.functions.validator.name_validator import validate_special_character
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)


# * <<----------------------------- *** Manufacturer Category Choices ***----------------------------->>
class ManufacturerCategoryChoices(TextChoices):
    """
    Manufacturer Category Choices
    """

    LOCAL = "local", "Local"
    FOREIGN = "foreign", "Foreign"


# * <<----------------------------- *** Manufacturer Product Category Table***----------------------------->>
class ManufacturerProductCategory(DjangoBaseModel):
    """
    Manufacturer Product Category Model
    """

    product_category = CharField(max_length=255, unique=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Manufacturer Product Category"
        verbose_name_plural = "Manufacturer Product Category"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["product_category"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "manufacturer_products_category"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure product_category is unique.
        Raises a ValidationError if a product category with the same name already exists.
        """
        # Check if a product category with the same name already exists
        if (
            ManufacturerProductCategory.objects.filter(
                product_category__iexact=self.product_category
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                {
                    "product_category": "A product category with this name already exists."
                },
            )

        # Check any special character exist in the product_category name
        if self.product_category:
            validate_special_character(
                self.product_category,
                field_name="product_category",
            )  # Validate product_category name for special characters
        else:
            raise ValidationError(
                {"product_category": "Product category name cannot be empty."},
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
        return f"{self.product_category}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<ManufacturerProductCategory: {self.product_category}> <id: {self.id}"


# * <<------------------------------*** Manufacturer Table ***--------------------------------------->>
class Manufacturer(DjangoBaseModel):
    """
    Manufacturer Model
    """

    product_category = ManyToManyField(
        ManufacturerProductCategory, related_name="manufacturer_product_category"
    )
    manufacturer_name = CharField(max_length=255, unique=True)
    manufacturer_logo = ImageField(upload_to="manufacturer/", blank=True, null=True)
    contact_person = CharField(max_length=255, blank=True, null=True)
    manufacturer_email = EmailField(max_length=255, blank=True, null=True)
    manufacturer_phone = PhoneNumberField(blank=True, null=True)
    manufacturer_address = TextField(blank=True, null=True)
    manufacturer_category = CharField(
        max_length=10,
        choices=ManufacturerCategoryChoices.choices,
        default=ManufacturerCategoryChoices.LOCAL,
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
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturer"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["manufacturer_name"]),
            Index(fields=["manufacturer_email"]),
            Index(fields=["manufacturer_phone"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "manufacturer"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure manufacturer_name is unique.
        Raises a ValidationError if a manufacturer with the same name already exists.
        """
        # Check if a manufacturer with the same name already exists
        if (
            Manufacturer.objects.filter(
                manufacturer_name__iexact=self.manufacturer_name
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                {
                    "manufacturer_name": "A manufacturer with this name already exists.",
                },
            )

        # Check any special character exist in the manufacturer_name name
        if self.manufacturer_name:
            validate_special_character(
                self.manufacturer_name,
                field_name="manufacturer_name",
            )  # Validate manufacturer_name name for special characters
        else:
            raise ValidationError(
                {"manufacturer_name": "Manufacturer name cannot be empty."},
            )

        # Validate the manufacturer_logo field
        if self.manufacturer_logo:
            get_validate_image_extensions(
                self.manufacturer_logo, allowed_extensions=["jpg", "jpeg", "png"]
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
        return f"{self.manufacturer_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<Manufacturer: {self.manufacturer_name}> <id: {self.id}"
