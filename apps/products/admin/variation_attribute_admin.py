from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.variation_attribute_model import (
    VariationAttribute,
    VariationAttributeValue,
)


# * <<-------------------------------------*** VariationAttribute Admin ***-------------------------------------->>
@register(VariationAttribute)
class VariationAttributeAdmin(ModelAdmin):
    """
    Admin interface for the VariationAttribute model.
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


# * <<-------------------------------------*** VariationAttributeValue Admin ***-------------------------------------->>
@register(VariationAttributeValue)
class VariationAttributeValueAdmin(ModelAdmin):
    """
    Admin interface for the VariationAttributeValue model.
    """

    list_display = (
        "id",
        "variation_attribute__id",
        "variation_attribute",
        "attribute_value",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "attribute_value",
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
        "variation_attribute__id",
        "variation_attribute__attribute_name",
        "attribute_value",
    )
    ordering = ("-id",)
    list_per_page = 50
