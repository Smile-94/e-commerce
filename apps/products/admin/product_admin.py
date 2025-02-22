from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

from apps.products.models.product_model import Product


# * <<-------------------------------------*** Product Admin ***-------------------------------------->>
@register(Product)
class ProductAdmin(ModelAdmin):
    """
    Admin interface for the Product model.
    """

    list_display = (
        "id",
        "product_id",
        "product_name",
        "product_type",
        "purchase_vat",
        "sales_vat",
        "product_unit",
        "brand",
        "manufacturer",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "product_name",
    )
    list_filter = (
        "product_type",
        "barcode_type",
        "active_status",
        ("created_at", DateFieldListFilter),
        ("created_at", DateFieldListFilter),
        (
            "created_at",
            DateRangeFilterBuilder(
                title="Create Date Range",
            ),
        ),
    )
    search_fields = (
        "id",
        "product_id",
        "product_name",
    )
    ordering = ("-id",)
    list_per_page = 50
