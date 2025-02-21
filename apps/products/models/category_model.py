from django.core.exceptions import ValidationError
from django.db.models import (
    BooleanField,
    CharField,
    ImageField,
    Index,
    PositiveIntegerField,
    TextField,
)

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
            Category.objects.filter(category_name__iexact=self.category_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                {"category_name": "A category with this name already exists."}
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
