from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    ImageField,
    Index,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from apps.common.functions.validator.image_validator import (
    get_validate_image_extensions,
)
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)
from apps.products.models.product_model import Product


# * <<--------------------------------------*** Product Image Gallery Table ***--------------------------------------->>
class ProductImageGallery(DjangoBaseModel):
    """
    Product Image Gallery Table
    """

    product = ForeignKey(
        Product,
        on_delete=CASCADE,
        related_name="product_image_gallery",
        help_text="Product Image Gallery",
    )
    product_image = ImageField(upload_to="product/")
    image_alt_name = CharField(max_length=255, blank=True, null=True)
    image_seo_tags = TextField(blank=True, null=True)
    image_meta_tags = TextField(blank=True, null=True)
    image_meta_description = TextField(blank=True, null=True)
    image_seo_description = TextField(blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Product Image Gallery"
        verbose_name_plural = "Product Image Gallery"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["product_id"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "product_image_gallery"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure product_image is not null.
        Raises a ValidationError if product_image is null.
        """
        if self.product_image is None:
            raise ValidationError(
                _("Product Image is required."),
            )
        # Validate image extensions
        if self.product_image:
            get_validate_image_extensions(
                self.product_image, allowed_extensions=[".jpg", ".png"]
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
        return f"{self.product.product_name}({self.id})"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<ProductImageGallery: {self.product.product_name}> <id: {self.id}"
