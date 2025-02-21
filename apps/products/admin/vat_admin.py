from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.vat_model import Vat


# * <<-------------------------------------*** Vat Admin ***-------------------------------------->>
@register(Vat)
class VatAdmin(ModelAdmin):
    """
    Admin interface for the Vat model.
    """

    list_display = (
        "id",
        "vat_amount",
        "value_type",
        "active_status",
        "created_at",
        "updated_at",
    )

    list_display_links = ("id",)
    list_filter = (
        "value_type",
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
        "vat_amount",
    )
    ordering = ("-id",)
    list_per_page = 50
