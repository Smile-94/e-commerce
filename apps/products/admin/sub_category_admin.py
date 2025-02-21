from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.sub_category_model import SubCategory


# * <<-------------------------------------*** Category Admin ***-------------------------------------->>
@register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    """
    Admin interface for the SubCategory model.
    """

    list_display = (
        "id",
        "sub_category_name",
        "category__id",
        "category",
        "parent_id",
        "is_client_usable",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "sub_category_name",
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
        "sub_category_name",
        "category__category_name",
    )
    ordering = ("-id",)
    list_per_page = 50
