from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.manufacturer_model import (
    Manufacturer,
    ManufacturerProductCategory,
)


# * <<-------------------------------------*** Manufacturer Product Category Admin ***-------------------------------------->>
@register(ManufacturerProductCategory)
class ManufacturerProductCategoryAdmin(ModelAdmin):
    """
    Admin interface for the Manufacturer model.
    """

    list_display = (
        "id",
        "product_category",
        "active_status",
        "description",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "product_category",
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
        "product_category",
    )
    ordering = ("-id",)
    list_per_page = 50


# * <<------------------------------------------------*** Manufacturer Admin ***-------------------------------->>
@register(Manufacturer)
class ManufacturerAdmin(ModelAdmin):
    """
    Admin interface for the Manufacturer model.
    """

    list_display = (
        "id",
        "manufacturer_name",
        "contact_person",
        "manufacturer_email",
        "manufacturer_phone",
        "manufacturer_category",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "manufacturer_name",
    )
    list_filter = (
        "manufacturer_category",
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
        "manufacturer_name",
    )
    ordering = ("-id",)
    list_per_page = 50
