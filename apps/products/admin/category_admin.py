from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models import Category


# * <<-------------------------------------*** Category Admin ***-------------------------------------->>
@register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Admin interface for the Category model.
    """

    list_display = (
        "id",
        "category_name",
        "parent_id",
        "is_client_usable",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "category_name",
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
        "category_name",
    )
    ordering = ("-id",)
    list_per_page = 50
