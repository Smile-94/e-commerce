from apps.common.dataclass.response_dataclass import (
    ErrorResponse,
    SuccessResponse,
    UpdateResponse,
)

# Import Documentation
from apps.common.documentation.documentation import (
    ResponseAPIDocumentation,
)
from apps.products.serializers.brand_serializer import BrandSerializer


class BrandDocumentationSchema:
    MODEL_NAME = "Brand"
    TAG_NAME = "Brand [V1]"

    @classmethod
    def get_create_schema(cls):
        return {
            "summary": f"API endpoint for creating product {cls.MODEL_NAME}",
            "description": f"Provide all necessary fields and values to create product {cls.MODEL_NAME}",
            "tags": [cls.TAG_NAME],
            "request": BrandSerializer,
            "responses": {
                "201": SuccessResponse,
                "400": ErrorResponse,
                "500": ErrorResponse,
            },
            "methods": ["POST"],
            "examples": [
                ResponseAPIDocumentation.get_201_response(
                    example={
                        "id": 1,
                        "brand_name": "My Brand",
                        "origin_country": "Bangladesh",
                        "web_url": "https://www.my-brand.com",
                        "brand_logo": "/brand/brand.jpg",
                        "contact_number": "+8801981000000",
                        "brand_email": "my@my-brand.com",
                        "description": "This category contains medicines.",
                        "active_status": "active",
                        "created_at": "2024-10-29",
                    },
                ),
                ResponseAPIDocumentation.get_400_response(),
                ResponseAPIDocumentation.get_500_response(),
            ],
        }

    @classmethod
    def get_update_schema(cls):
        return {
            "summary": f"API endpoint for updating product {cls.MODEL_NAME}",
            "description": f"Provide all necessary fields and values to update product {cls.MODEL_NAME}",
            "tags": [cls.TAG_NAME],
            "request": BrandSerializer(partial=True),
            "responses": {
                "200": UpdateResponse,
                "400": ErrorResponse,
                "500": ErrorResponse,
            },
            "methods": ["PATCH", "PUT"],
            "examples": [
                ResponseAPIDocumentation.get_200_response(
                    message=f"{cls.MODEL_NAME} Updated Successfully",
                    example={
                        "info": "following fields are updated",
                        "fields": ["brand_name", "brand_icon"],
                    },
                ),
                ResponseAPIDocumentation.get_404_response(),
                ResponseAPIDocumentation.get_400_response(),
                ResponseAPIDocumentation.get_500_response(),
            ],
        }
