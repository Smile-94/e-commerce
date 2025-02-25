from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.medicines.models.generic_name_model import GenericNameInformation


# * <<-------------------------------------*** Generic Name Information Admin ***-------------------------------------->>
@register(GenericNameInformation)
class GenericNameInformationAdmin(ModelAdmin):
    """
    Admin interface for the GenericNameInformation model.
    """

    list_display = (
        "id",
        "generic_name",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "generic_name",
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
        "generic_name",
    )
    ordering = ("-id",)
    list_per_page = 50
