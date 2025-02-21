from drf_spectacular.utils import OpenApiExample, OpenApiParameter
from rest_framework import status


class ResponseAPIDocumentation:
    @staticmethod
    def get_201_response(
        example={
            "id": 1,
            "name": "Category 1",
            "description": "Category Description 1",
            "created_at": "2022-01-01T00:00:00Z",
            "updated_at": "2022-01-01T00:00:00Z",
        },
    ):
        return OpenApiExample(
            "Success Response",
            value={
                "status": status.HTTP_201_CREATED,
                "message": "object created successfully",
                "client": "DEVELOPER",
                "data": [example],
                "links": {"list": "http://example.com"},
            },
            response_only=True,
            status_codes=[status.HTTP_201_CREATED],
        )

    @staticmethod
    def get_200_response(
        message: str = "object updated Successfully",
        example: dict = {"id": 1},
    ):
        return OpenApiExample(
            "Success Response",
            value={
                "status": status.HTTP_200_OK,
                "message": message,
                "client": "USER",
                "data": [example],
                "links": {"list": "http://example.com"},
            },
            response_only=True,
            status_codes=[status.HTTP_200_OK],
        )

    @staticmethod
    def get_204_response(message):
        return OpenApiExample(
            "No Content Response",
            value={
                "status": status.HTTP_204_NO_CONTENT,
                "message": f"{message}",
                "client": "DEVELOPER",
                "data": None,
            },
            response_only=True,
            status_codes=[status.HTTP_200_OK],
        )

    @staticmethod
    def get_400_response():
        return OpenApiExample(
            "Bad Request",
            value={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid fields",
                "client": "DEVELOPER",
                "details": {"field_name": ["invalid_field"]},
            },
            response_only=True,
            status_codes=[status.HTTP_400_BAD_REQUEST],
        )

    @staticmethod
    def get_404_response():
        return OpenApiExample(
            "Not Found",
            value={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Given Content not found",
                "client": "DEVELOPER",
                "details": {"field_name": "No content found with the provided ID"},
            },
            response_only=True,
            status_codes=[status.HTTP_404_NOT_FOUND],
        )

    @staticmethod
    def get_500_response():
        return OpenApiExample(
            "Internal Server Error",
            value={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An server side error occurred while processing your request",
                "client": "DEVELOPER",
                "details": {"error": "got and unexpected keyword arguments"},
            },
            response_only=True,
            status_codes=[status.HTTP_500_INTERNAL_SERVER_ERROR],
        )


class ParameterAPIDocumentation:
    @staticmethod
    def get_limit_parameter():
        return OpenApiParameter(
            "limit",
            type=int,
            description="Number of items per page",
            examples=[
                OpenApiExample(
                    "Limit Example",
                    value=10,
                ),
            ],
        )

    @staticmethod
    def get_offset_parameter():
        return OpenApiParameter(
            name="offset",
            type=int,
            description="Starting point for fetching items, integer",
            examples=[OpenApiExample("Offset Example", value=0)],
        )

    @staticmethod
    def get_field_list_parameter(
        fields_list: str = "id,",
        example_value: str = "id",
        field_name: str = "field_list",
    ):
        return OpenApiParameter(
            name=field_name,
            type=str,
            description=f"Comma-separated list of fields to get data by (e.g., {fields_list})",
            examples=[OpenApiExample("Field List Example", value=f"{example_value}")],
        )

    @staticmethod
    def get_ordering_parameter(
        ordering_fields: str = "id,",
        example_value: str = "id,",
    ):
        return OpenApiParameter(
            name="ordering",
            type=str,
            description=f"Comma-separated list of fields to include or order by (e.g., {ordering_fields})",
            examples=[
                OpenApiExample(
                    "Ordering Example",
                    value=f"{example_value}",
                ),
            ],
        )

    @staticmethod
    def get_query_parameter(
        supported_fields: str = "name",
        example_value: str = "Don Joe",
    ):
        return OpenApiParameter(
            name="query",
            type=str,
            description=f"Search query string, supports fields= {supported_fields}",
            examples=[
                OpenApiExample(
                    "Query Example",
                    value=example_value,
                ),
            ],
        )

    @staticmethod
    def get_from_date_parameter(
        supported_fields: str = "created_at",
        example_value: str = "2024-11-11",
    ):
        return OpenApiParameter(
            name="from_date",
            type=str,
            description=f"Search query string, supports fields= {supported_fields}",
            examples=[
                OpenApiExample(
                    "Query Example",
                    value=example_value,
                ),
            ],
        )

    @staticmethod
    def get_to_date_parameter(
        supported_fields: str = "created_at",
        example_value: str = "2024-11-11",
    ):
        return OpenApiParameter(
            name="to_date",
            type=str,
            description=f"Search query string, supports fields= {supported_fields}",
            examples=[
                OpenApiExample(
                    "Query Example",
                    value=example_value,
                ),
            ],
        )

    @staticmethod
    def get_active_status_parameter(
        supported_fields: str = "active_status",
        example_value: str = "active",
    ):
        return OpenApiParameter(
            name="active_status",
            type=str,
            description=f"Search query string, supports fields= {supported_fields}",
            examples=[
                OpenApiExample(
                    "Query Example",
                    value=example_value,
                ),
            ],
        )
