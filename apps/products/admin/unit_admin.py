from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.unit_model import (
    UnitAttribute,
    UnitAttributeValue,
)


# * <<-------------------------------------*** Unit Attribute Admin ***-------------------------------------->>
@register(UnitAttribute)
class UnitAttributeAdmin(ModelAdmin):
    """
    Admin interface for the UnitAttribute model.
    """

    list_display = (
        "id",
        "attribute_name",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "attribute_name",
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
        "attribute_name",
    )
    ordering = ("-id",)
    list_per_page = 50


# * <<---------------------------------------------*** Unit Attribute Value Admin ***-------------------->>
@register(UnitAttributeValue)
class UnitAttributeValueAdmin(ModelAdmin):
    """
    Admin interface for the UnitAttributeValue model.
    """

    list_display = (
        "id",
        "unit_attribute__id",
        "unit_attribute",
        "unit_value",
        "active_status",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "unit_value",
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
        "unit_attribute__attribute_name",
        "unit_value",
    )
    ordering = ("-id",)
    list_per_page = 50
