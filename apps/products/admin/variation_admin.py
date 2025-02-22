from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.variation_model import ProductVariation


# * <<-------------------------------------*** Product Variation Admin ***-------------------------------------->>
@register(ProductVariation)
class ProductVariationAdmin(ModelAdmin):
    """
    Admin interface for the ProductVariation model.
    """

    list_display = (
        "id",
        "variation_name",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "variation_name",
    )
    list_filter = (
        "active_status",
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
        "variation_name",
    )
    ordering = ("-id",)
    list_per_page = 50
