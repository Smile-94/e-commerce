from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

from apps.products.models.image_gallery_model import ProductImageGallery


# * <<-------------------------------------*** Product Image Gallery Admin ***-------------------------------------->>
@register(ProductImageGallery)
class ProductImageGalleryAdmin(ModelAdmin):
    list_display = (
        "id",
        "product",
        "created_at",
        "updated_at",
        "active_status",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "id",
        "product",
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
        "product__id",
        "product__product_name",
    )
    ordering = ("-id",)
    list_per_page = 50
