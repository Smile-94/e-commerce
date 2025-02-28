from django.urls import include, path

from apps.products.urls import (
    brand_url,
    category_url,
)

# * <<-------------------------------------*** Product API Router ***-------------------------------------->>
urlpatterns = [
    path("products/brand/", include(brand_url)),  # product brand api router
    path("products/category/", include(category_url)),  # product category api router
]
