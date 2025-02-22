from django.core.exceptions import ValidationError
from django.db.models import (
    SET_NULL,
    CharField,
    ForeignKey,
    ImageField,
    Index,
    ManyToManyField,
    TextChoices,
    TextField,
)
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from apps.common.functions.barcode_methods import (
    get_generated_barcode,
)
from apps.common.functions.custom_id import (
    get_generated_custom_id,
)
from apps.common.functions.validator.image_validator import (
    get_validate_image_extensions,
)
from apps.common.functions.validator.name_validator import (
    validate_special_character,
)
from apps.common.models import (
    ActiveStatusChoices,
    DjangoBaseModel,
)
from apps.products.function.url_slug_method import get_generated_slug
from apps.products.models.brand_model import Brand
from apps.products.models.manufacturer_model import Manufacturer
from apps.products.models.sub_category_model import SubCategory
from apps.products.models.unit_model import UnitAttributeValue
from apps.products.models.vat_model import Vat


# * Product Type Choices
class ProductTypeChoices(TextChoices):
    """
    Product Type Choices
    """

    MEDICINE = "medicine", _("Medicine")
    DEVICE = "device", _("Device")
    SERVICE = "service", _("Service")
    GENERAL = "general", _("General")
    BOOK = "book", _("Book")
    OTHER = "other", _("Other")


# * Product Barcode Choices
class ProductBarcodeChoices(TextChoices):
    """
    Product Barcode Choices
    """

    MANUAL = "manual", _("Manual")
    AUTO = "auto", _("Auto")


# * <<--------------------------------------*** Product Table ***--------------------------------------->>
class Product(DjangoBaseModel):
    """
    Product Table
    """

    product_id = CharField(max_length=30, unique=True)
    product_name = CharField(max_length=255)
    sub_category = ManyToManyField(
        SubCategory,
        related_name="product_sub_category",
        blank=True,
    )
    product_type = CharField(
        max_length=30,
        choices=ProductTypeChoices.choices,
        default=ProductTypeChoices.GENERAL,
        blank=True,
        null=True,
    )
    product_image = ImageField(upload_to="product/", blank=True, null=True)
    image_alt_name = CharField(max_length=255)
    barcode_type = CharField(
        max_length=10,
        choices=ProductBarcodeChoices.choices,
        default=ProductBarcodeChoices.MANUAL,
        blank=True,
        null=True,
    )
    barcode = CharField(max_length=255, unique=True, blank=True, null=True)
    purchase_vat = ForeignKey(
        Vat,
        on_delete=SET_NULL,
        related_name="purchase_vat_amount",
        blank=True,
        null=True,
    )
    sales_vat = ForeignKey(
        Vat,
        on_delete=SET_NULL,
        related_name="sales_vat_amount",
        blank=True,
        null=True,
    )
    product_unit = ForeignKey(
        UnitAttributeValue,
        related_name="product_unit",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )
    brand = ForeignKey(
        Brand,
        on_delete=SET_NULL,
        related_name="product_brand",
        blank=True,
        null=True,
    )
    manufacturer = ForeignKey(
        Manufacturer,
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )
    url_slug = CharField(max_length=255, blank=True, null=True)
    search_keyword = TaggableManager(blank=True, verbose_name="search_keyword")
    description = TextField(blank=True, null=True)
    active_status = CharField(
        max_length=10,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product"
        ordering = ["-id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["product_id"]),
            Index(fields=["product_type"]),
            Index(fields=["barcode"]),
            Index(fields=["brand"]),
            Index(fields=["manufacturer"]),
            Index(fields=["active_status"]),
        ]
        app_label = "products"
        db_table = "product"

    def clean(self):
        """
        Custom validation to ensure product_name is unique.
        Raises a ValidationError if a product with the same name already exists.
        """
        if self.__class__.objects.filter(product_name=self.product_name).exists():
            raise ValidationError(
                _("Product name already exists."),
            )

        if not self.product_id:
            self.product_id = get_generated_custom_id(
                id_prefix="PRO",
                model_class=self.__class__,
                field="product_id",
            )

        # Validate product_name
        if self.product_name:
            validate_special_character(self.product_name)
        else:
            raise ValidationError({_("Product name cannot be empty.")})

        # Validate product_image
        if self.product_image:
            get_validate_image_extensions(
                self.product_image, allowed_extensions=[".jpg", ".png"]
            )

        # generate barcode
        if not self.barcode:
            if self.barcode_type == ProductBarcodeChoices.AUTO:
                if self.product_id:
                    self.barcode = get_generated_barcode(self.product_id)

        if not self.url_slug:
            self.url_slug = get_generated_slug(
                self.product_name,
                self.product_unit,
                self.product_unit.unit_attribute.attribute_name,
            )

        super().clean()

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
        if self.product_unit:
            return f"{self.product_name} ({self.product_unit.unit_value}{self.product_unit.unit_attribute.attribute_name})"

        else:
            return f"{self.product_name}"

    # Return a string representation of the model instance
    def __repr__(self):
        return f"<Product: {self.product_name}> <id: {self.id}"
