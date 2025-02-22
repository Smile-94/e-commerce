from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.brand_model import Brand


# * <<-------------------------------------*** Brand Admin ***-------------------------------------->>
@register(Brand)
class BrandAdmin(ModelAdmin):
    """
    Admin interface for the Brand model.
    """

    list_display = (
        "id",
        "brand_name",
        "origin_country",
        "contact_number",
        "brand_email",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "brand_name",
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
        "brand_name",
        "origin_country",
    )
    ordering = ("-id",)
    list_per_page = 50
