from apps.products.admin.brand_admin import BrandAdmin
from apps.products.admin.category_admin import CategoryAdmin
from apps.products.admin.image_gallery_admin import ProductImageGalleryAdmin
from apps.products.admin.manufacturer_admin import (
    ManufacturerAdmin,
    ManufacturerProductCategoryAdmin,
)
from apps.products.admin.product_admin import ProductAdmin
from apps.products.admin.product_seo_admin import ProductSeoAdmin
from apps.products.admin.sub_category_admin import SubCategoryAdmin
from apps.products.admin.unit_admin import (
    UnitAttributeAdmin,
    UnitAttributeValueAdmin,
)
from apps.products.admin.variation_admin import ProductVariationAdmin
from apps.products.admin.variation_attribute_admin import (
    VariationAttributeAdmin,
    VariationAttributeValueAdmin,
)
from apps.products.admin.vat_admin import VatAdmin

__all__ = [
    "CategoryAdmin",
    "SubCategoryAdmin",
    "UnitAttributeAdmin",
    "UnitAttributeValueAdmin",
    "BrandAdmin",
    "ManufacturerProductCategoryAdmin",
    "ManufacturerAdmin",
    "VatAdmin",
    "ProductAdmin",
    "ProductImageGalleryAdmin",
    "ProductSeoAdmin",
    "VariationAttributeAdmin",
    "VariationAttributeValueAdmin",
    "ProductVariationAdmin",
    # Add more admin classes here if needed.
]
