from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    ImageField,
    Index,
    PositiveIntegerField,
    TextField,
)

from apps.common.functions.validator.image_validator import (
    get_validate_image_extensions,
)
from apps.common.functions.validator.name_validator import validate_special_character
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)
from apps.products.models.category_model import Category


# * <<-------------------------------------*** Product Sub-Category Model ***------------------------------------->>
class SubCategory(DjangoBaseModel):
    """
    Product Sub-Category Model
    """

    category = ForeignKey(
        Category, on_delete=CASCADE, related_name="sub_category_category"
    )
    sub_category_name = CharField(max_length=255, unique=True)
    parent_id = PositiveIntegerField(default=0, blank=True)
    sub_category_icon = ImageField(
        upload_to="product/sub_categories", blank=True, null=True
    )
    is_client_usable = BooleanField(default=False, blank=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Sub-Category"
        verbose_name_plural = "Sub-Category"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["sub_category_name"]),
            Index(fields=["is_client_usable"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "sub_category"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure sub_category_name is unique.
        Raises a ValidationError if a sub-category with the same name already exists.
        """
        # Check if a sub-category with the same name already exists
        if (
            self.__class__.objects.filter(
                sub_category_name__iexact=self.sub_category_name
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                {"sub_category_name": "A sub-category with this name already exists."},
            )

        # Check any special character exist in the sub-category name
        if self.sub_category_name:
            validate_special_character(
                self.sub_category_name,
                field_name="sub_category_name",
            )  # Validate sub_category_name for special characters
        else:
            raise ValidationError(
                {"sub_category_name": "Sub-category name cannot be empty."},
            )

        # Ensure sub_category_icon is a valid image file
        if self.sub_category_icon:
            get_validate_image_extensions(
                images=[
                    self.sub_category_icon,
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
        return f"{self.sub_category_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<SubCategory: {self.sub_category_name}> <id: {self.id}"
