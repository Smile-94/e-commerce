from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.medicines.models.medicine_info_model import MedicineInfo


# * <<-------------------------------------*** Medicine Info Admin ***-------------------------------------->>
@register(MedicineInfo)
class MedicineInfoAdmin(ModelAdmin):
    """
    Admin interface for the MedicineInfo model.
    """

    list_display = (
        "id",
        "product__id",
        "product",
        "is_required_prescription",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    list_filter = (
        "is_required_prescription",
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
        "product__product_name",
    )
    ordering = ("-id",)
    list_per_page = 50
