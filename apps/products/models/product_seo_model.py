from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    CharField,
    Index,
    OneToOneField,
    TextField,
)
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from apps.common.functions.validator.name_validator import (
    validate_special_character,
)
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)
from apps.products.models.product_model import Product


# * <<-------------------------------------*** Product Image Gallery Model ***-------------------------------------->>
class ProductSeo(DjangoBaseModel):
    """
    Product SEO Table
    """

    product = OneToOneField(
        Product,
        on_delete=CASCADE,
        related_name="product_seo",
    )
    seo_title = CharField(max_length=255, unique=True)
    seo_keyword = TaggableManager(blank=True, verbose_name="seo_keyword")
    meta_tags = TextField(blank=True, null=True)
    meta_description = TextField(blank=True, null=True)
    seo_description = TextField(blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Product SEO"
        verbose_name_plural = "Product SEO"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["product_id"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "product_seo"

    # Clean up the instance before saving
    def clean(self):
        """
        Custom validation to ensure seo_title is unique.
        Raises a ValidationError if a seo with the same seo_title already exists.
        """
        # Check if a seo with the same seo_title already exists
        if (
            self.__class__.objects.filter(seo_title__iexact=self.seo_title)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                _("A seo with this title already exists."),
            )

        # Validate special characters in seo_title
        validate_special_character(self.seo_title)

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
        return f"{self.seo_title}({self.id})"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<ProductSeo: {self.product.product_name}> <id: {self.id}"
