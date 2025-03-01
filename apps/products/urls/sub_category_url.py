from django.urls import path

# Import views
from apps.products.apis.sub_category_api import (
    CreateProductSubCategoryAPIView,
    DeleteProductSubCategoryAPIView,
    ListProductSubCategoryAPIView,
    RetrieveProductSubCategoryAPIView,
    UpdateProductSubCategoryAPIView,
)

# * <<-------------------------------------*** Product Sub-Category API Router ***-------------------------------------->>
urlpatterns = [
    path(
        "create/",
        CreateProductSubCategoryAPIView.as_view(),
        name="create_product_sub_category",
    ),  # create product sub-category api endpoint
    path(
        "update/<int:id>/",
        UpdateProductSubCategoryAPIView.as_view(),
        name="update_product_sub_category",
    ),  # update product sub-category api endpoint
    path(
        "list/",
        ListProductSubCategoryAPIView.as_view(),
        name="list_product_sub_category",
    ),  # list product sub-category api endpoint
    path(
        "details/<int:id>/",
        RetrieveProductSubCategoryAPIView.as_view(),
        name="retrieve_product_sub_category",
    ),  # retrieve product sub-category api endpoint
    path(
        "delete/<int:id>/",
        DeleteProductSubCategoryAPIView.as_view(),
        name="delete_product_sub_category",
    ),  # delete product sub-category api endpoint
]
