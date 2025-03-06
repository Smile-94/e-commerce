from django.urls import path

# Import views
from apps.products.apis.manufacturer_product_category_api import (
    CreateManufacturerProductCategoryAPIView,
    DeleteManufacturerProductCategoryAPIView,
    ListManufacturerProductCategoryAPIView,
    RetrieveManufacturerProductCategoryAPIView,
    UpdateManufacturerProductCategoryAPIView,
)

# * <<-------------------------------------*** Manufacturer Product Category API Router ***-------------------------------------->>
urlpatterns = [
    path(
        "product-category/create/",
        CreateManufacturerProductCategoryAPIView.as_view(),
        name="create_manufacturer_product_category",
    ),  # create manufacturer product category api endpoint
    path(
        "product-category/update/<int:id>/",
        UpdateManufacturerProductCategoryAPIView.as_view(),
        name="update_manufacturer_product_category",
    ),  # update manufacturer product category api endpoint
    path(
        "product-category/list/",
        ListManufacturerProductCategoryAPIView.as_view(),
        name="list_manufacturer_product_category",
    ),  # list manufacturer product category api endpoint
    path(
        "product-category/details/<int:id>/",
        RetrieveManufacturerProductCategoryAPIView.as_view(),
        name="retrieve_manufacturer_product_category",
    ),  # retrieve manufacturer product category api endpoint
    path(
        "product-category/delete/<int:id>/",
        DeleteManufacturerProductCategoryAPIView.as_view(),
        name="delete_manufacturer_product_category",
    ),  # delete manufacturer product category api endpoint
]
