from django.contrib.admin import (
    DateFieldListFilter,
    ModelAdmin,
    # Methods
    register,
)
from rangefilter.filters import DateRangeFilterBuilder

# Import Models
from apps.products.models.product_seo_model import ProductSeo


# * <<-------------------------------------*** ProductSeo Admin ***-------------------------------------->>
@register(ProductSeo)
class ProductSeoAdmin(ModelAdmin):
    """
    Admin interface for the ProductSeo model.
    """

    list_display = (
        "id",
        "product__id",
        "product",
        "seo_title",
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
        "seo_title",
    )
    ordering = ("-id",)
    list_per_page = 50
