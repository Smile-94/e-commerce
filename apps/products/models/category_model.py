from django.core.exceptions import ValidationError
from django.db.models import (
    BooleanField,
    CharField,
    ImageField,
    Index,
    PositiveIntegerField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from apps.common.functions.validator.image_validator import (
    get_validate_image_extensions,
)
from apps.common.functions.validator.name_validator import validate_special_character
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)


# * <<--------------------------------------*** Product Category Table ***--------------------------------------->>
class Category(DjangoBaseModel):
    """
    product Category Table
    """

    category_name = CharField(max_length=255, unique=True)
    parent_id = PositiveIntegerField(default=0, blank=True)
    is_client_usable = BooleanField(default=False, blank=True)
    category_icon = ImageField(upload_to="product/categories", blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )
    description = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["category_name"]),
            Index(fields=["is_client_usable"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "category"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure category_name is unique.
        Raises a ValidationError if a category with the same name already exists.
        """
        # Check if a category with the same name already exists
        if (
            self.__class__.objects.filter(category_name__iexact=self.category_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                _("A category with this name already exists."),
            )

        # Check any special character exist in the category name
        if self.category_name:
            validate_special_character(
                self.category_name, field_name="category_name"
            )  # Validate category_name for special characters
        else:
            raise ValidationError(
                _(
                    "Category name cannot be empty.",
                )
            )

        # Ensure category_icon is a valid image file
        if self.category_icon:
            get_validate_image_extensions(
                images=[
                    self.category_icon,
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
        return f"{self.category_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<Category: {self.category_name}> <id: {self.id}"
