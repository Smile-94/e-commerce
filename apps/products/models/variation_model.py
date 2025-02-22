from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    ImageField,
    Index,
    ManyToManyField,
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
from apps.products.models.product_model import Product
from apps.products.models.variation_attribute_model import VariationAttributeValue


# * <<-------------------------------------*** Product Variation Model ***-------------------------------------->>
class ProductVariation(DjangoBaseModel):
    """
    Product Variation Model
    """

    product = ForeignKey(Product, on_delete=CASCADE, related_name="variation_product")
    variation_attribute = ManyToManyField(
        VariationAttributeValue, related_name="product_variation_attribute"
    )
    variation_name = CharField(max_length=255, unique=True, blank=True, null=True)
    variation_image = ImageField(upload_to="product/", blank=True, null=True)
    image_alt_name = CharField(max_length=255, blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Product Variation"
        verbose_name_plural = "Product Variations"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["variation_name"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "product_variation"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure variation_name is unique.
        Raises a ValidationError if a variation with the same name already exists.
        """
        # Check if a variation with the same name already exists
        if (
            self.__class__.objects.filter(
                variation_name__iexact=self.variation_name, product_id=self.product_id
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                _("A variation with this name already exists."),
            )

        # Check any special character exist in the variation_name
        if self.variation_name:
            validate_special_character(
                self.variation_name,
                field_name="variation_name",
            )  # Validate variation_name for special characters
        else:
            raise ValidationError(
                _("Variation name cannot be empty."),
            )

        # Ensure variation_image is a valid image file
        if self.variation_image:
            get_validate_image_extensions(
                images=[
                    self.variation_image,
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

    def __str__(self):
        return f"{self.variation_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<ProductVariation: {self.variation_name}>"
