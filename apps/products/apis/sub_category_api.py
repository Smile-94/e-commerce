from drf_spectacular.utils import extend_schema
from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.dataclass.response_dataclass import (
    ErrorResponse,
    ErrorType,
    NoContentResponse,
    ResponseClient,
    SuccessResponse,
    UpdateResponse,
)

# Import Documentation
from apps.common.documentation.documentation import (
    ParameterAPIDocumentation,
    ResponseAPIDocumentation,
)
from apps.common.functions.api_allowed_method import allowed_methods
from apps.common.functions.response_links import get_response_links
from apps.common.functions.valid_query_params import get_valid_query_params
from apps.common.functions.validator.field_validator import (
    get_model_fields,
    get_validated_choices_field,
    get_validated_request_fields,
    get_validated_response_fields,
)
from apps.common.models import ActiveStatusChoices
from apps.common.pagination.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from apps.products.filters.sub_category_filter import SubCategorySearchFilter

# Models Import
from apps.products.models.category_model import Category
from apps.products.models.product_model import Product
from apps.products.models.sub_category_model import SubCategory

# Import Serializer
from apps.products.serializers.sub_category_serializer import (
    SubCategorySerializer,
    SubCategoryUpdateSerializer,
)

# API TAGS Name
MODEL_NAME = "Sub-Category"
URL_PREFIX = "sub-category"
TAG_NAME = "Sub-sCategory [v1]"


# * <<---------------------*** CREATE PRODUCT SUB-CATEGORY API VIEW ***--------------------->>
@allowed_methods("POST")
class CreateProductSubCategoryAPIView(APIView):
    """
    API endpoint to create a new product Category.
    """

    # TODO:
    # Add permissions Class

    def __init__(self, *args, **kwargs):
        self.model_class = SubCategory
        self.category_model = Category
        self.serializer_class = SubCategorySerializer
        super().__init__(*args, **kwargs)

    # API documentation
    @extend_schema(
        summary=f"API endpoint for creating product {MODEL_NAME}",
        description=f"Provide all necessary fields and values to create product {MODEL_NAME}",
        tags=[TAG_NAME],
        request=SubCategorySerializer,
        responses={
            "201": SuccessResponse,
            "400": ErrorResponse,
            "500": ErrorResponse,
        },
        examples=[
            ResponseAPIDocumentation.get_201_response(
                example={
                    "id": 1,
                    "created_at": "2025-02-28T20:08:40.434798Z",
                    "updated_at": "2025-02-28T20:08:40.434837Z",
                    "sub_category_name": "Capsule",
                    "parent_id": 0,
                    "sub_category_icon": "/media/product/sub_categories/medicine.png",
                    "is_client_usable": False,
                    "active_status": "active",
                    "description": "This is short but amazing description",
                    "category": {
                        "id": 1,
                        "category_name": "Medicine",
                    },
                },
            ),
            ResponseAPIDocumentation.get_400_response(),
            ResponseAPIDocumentation.get_500_response(),
        ],
    )
    # HTTP POST METHOD to Create
    def post(self, request, *args, **kwargs):
        try:
            if request.data:
                sub_category_name = request.data.get("sub_category_name", None)
                active_status = request.data.get("active_status", None)

                # Relation Fields
                category = request.data.get("category", None)

                # Get all valid field names from the brand model
                invalid_fields = get_validated_request_fields(
                    model_class=self.model_class,
                    request_data=request.data,
                )

                if invalid_fields:
                    logger.warning(
                        f"--------->>Invalid field names in request data: {invalid_fields}",
                    )
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid field names in request data",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_fields": invalid_fields,
                                "info": f"Some field names are not valid for the {self.model_class.__name__}",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Check required fields in request data
                if not sub_category_name:
                    logger.warning(
                        f"WARNING({self.__class__.__name__}):--------->> sub_category_name is required in request data."
                    )

                    # Return The required fields missing errors
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Sub-Category Name is required",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "sub_category_name": "sub_category_name missing",
                                "info": "'sub_category_name' is required to create new sub-category object",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Validate choices for active_status field
                if active_status:
                    is_valid, valid_choices = get_validated_choices_field(
                        choices_class=ActiveStatusChoices,
                        choices_value=active_status,
                    )

                    if not is_valid:
                        logger.warning(
                            f"WARNING({self.__class__.__name__})--------->>Invalid active_status: {active_status}",
                        )

                        # Return The Invalid Field Error Response
                        return Response(
                            ErrorResponse(
                                status=status.HTTP_400_BAD_REQUEST,
                                type=ErrorType.WARNING,
                                message="Invalid active_status",
                                client=ResponseClient.DEVELOPER,
                                description={
                                    "active_status": f"Must be one of {', '.join(valid_choices)}",
                                    "info": "Select active_status as 'active' or 'inactive'",
                                },
                            ).model_dump(),
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                invalid_relationship = []
                not_exist_relationship = []
                # check product relationship validity

                # Check product supplier relationship validity
                if category:
                    try:
                        object_id = int(category)
                        if object_id > 0:
                            if not self.category_model.objects.filter(
                                id=object_id
                            ).exists():
                                not_exist_relationship.append(
                                    {
                                        "category": object_id,
                                        "info": f"Category with id {object_id} not found",
                                    }
                                )
                    except ValueError:
                        invalid_relationship.append(
                            {
                                "category": category,
                                "info": "Invalid category id, category must be a positive integer",
                            },
                        )

                else:
                    logger.warning(
                        f"WARNING({self.__class__.__name__}):--------->> category is required in request data."
                    )

                    # Return The required fields missing errors
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Category is required",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "category": "category missing",
                                "info": "'category' is required to create new sub-category object",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if invalid_relationship:
                    logger.warning(
                        f"WARNING({self.__class__.__name__}):--------->> Invalid relationships: {invalid_relationship}",
                    )
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid relationships",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_relationships": invalid_relationship,
                                "info": "Check your relationships data with other objects",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not_exist_relationship:
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid relationship",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "not_exist_relationships": not_exist_relationship,
                                "info": "Check your relationships data with other objects",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Check the product name is exist or not, if not exist then create a new brand object
                if not self.model_class.objects.filter(
                    sub_category_name=sub_category_name
                ).exists():
                    # Parse and validate data using Pydantic
                    serializer = self.serializer_class(data=request.data)

                    if serializer.is_valid():
                        serializer.save()

                        if serializer:
                            # Return Success Response
                            return Response(
                                SuccessResponse(
                                    status=status.HTTP_201_CREATED,
                                    message=f"{self.model_class.__name__} Created Successfully",
                                    client=ResponseClient.USER,
                                    data=serializer.data,
                                    links=get_response_links(
                                        action="create", url_prefix=URL_PREFIX
                                    ),
                                ).model_dump(),
                                status=status.HTTP_201_CREATED,
                            )

                    else:
                        logger.error(
                            f"ERROR({self.__class__.__name__}): sub-Category create serializer error {serializer.errors}",
                        )

                        # Return Serializers Error Response
                        return Response(
                            ErrorResponse(
                                status=status.HTTP_400_BAD_REQUEST,
                                type=ErrorType.ERROR,
                                message="Data Validation Error",
                                client=ResponseClient.DEVELOPER,
                                description={
                                    "errors": serializer.errors,
                                    "info": "Check your request data and fix, provide valid data",
                                },
                            ).model_dump(),
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                else:
                    # Unique object warning response
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message=f"{self.model_class.__name__} name already exists",
                            client=ResponseClient.USER,
                            description={
                                "sub_category_name": f"{sub_category_name}",
                                "info": f"sub-category name '{sub_category_name}' already exists, try a different sub_category_name",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                return Response(
                    # Empty body data response
                    ErrorResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        type=ErrorType.WARNING,
                        message="No Data Provided, Please provide payload data",
                        client=ResponseClient.DEVELOPER,
                        description={
                            "category": "int, This field is required, provide a valid category id",
                            "sub_category_name": "str, This field is required",
                            "parent_id": "int, This field is not optional, default=0.",
                            "is_client_usable": "bool, This field is optional, default=False",
                            "sub_category_icon": "ImageField, optional",
                            "active_status": "choice, optional, default='active', and choices must be 'active', or 'inactive',",
                            "description": "str, optional",
                        },
                    ).model_dump(),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            logger.error(
                f"ERROR({self.__class__.__name__})----->>Error occurred while creating product sub-Category: {str(e)}",
            )
            # Un excepted error response
            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="An server side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": "An unexpected error occurred while creating sub-Category",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<---------------------*** UPDATE PRODUCT SUB-CATEGORY API VIEW ***--------------------->>
@allowed_methods("PUT", "PATCH")
class UpdateProductSubCategoryAPIView(APIView):
    """
    API endpoint to update an existing product category.
    """

    # TODO:
    # Add permissions Class

    def __init__(self, *args, **kwargs):
        self.model_class = SubCategory
        self.category_class = Category
        self.serializer_class = SubCategoryUpdateSerializer
        super().__init__(*args, **kwargs)

    # Update Product Category API Documentation.
    @extend_schema(
        summary=f"API endpoint for updating a product {MODEL_NAME}",
        description=f"Provide all necessary fields and values to update a product {MODEL_NAME}",
        tags=[TAG_NAME],
        request=SubCategoryUpdateSerializer,
        responses={
            "200": UpdateResponse,
            "400": ErrorResponse,
            "500": ErrorResponse,
        },
        examples=[
            ResponseAPIDocumentation.get_200_response(
                message=f"{MODEL_NAME} Updated Successfully",
                example={
                    "info": "following fields are updated",
                    "fields": ["category_name", "category_icon"],
                },
            ),
            ResponseAPIDocumentation.get_404_response(),
            ResponseAPIDocumentation.get_400_response(),
            ResponseAPIDocumentation.get_500_response(),
        ],
    )
    def put(self, request, id, *args, **kwargs):
        return self._update_category(request, id, partial=False)

    @extend_schema(
        summary=f"API endpoint for partially updating a product {MODEL_NAME}",
        description=f"Provide specific fields and values to update part of a product {MODEL_NAME}",
        tags=[TAG_NAME],
        request=SubCategoryUpdateSerializer,
        responses={
            "200": UpdateResponse,
            "400": ErrorResponse,
            "500": ErrorResponse,
        },
        examples=[
            ResponseAPIDocumentation.get_200_response(
                message=f"{MODEL_NAME} Partially Updated Successfully",
                example={
                    "info": "following fields are updated",
                    "fields": ["sub_category_name", "sub_category_icon"],
                },
            ),
            ResponseAPIDocumentation.get_404_response(),
            ResponseAPIDocumentation.get_400_response(),
            ResponseAPIDocumentation.get_500_response(),
        ],
    )
    def patch(self, request, id, *args, **kwargs):
        return self._update_category(request, id, partial=True)

    def _update_category(self, request, id, partial):
        try:
            if request.data:
                sub_category_name = request.data.get("sub_category_name", None)
                active_status = request.data.get("active_status", None)

                # Relationship fields
                category = request.data.get("category", None)

                invalid_fields = get_validated_request_fields(
                    model_class=self.model_class,
                    request_data=request.data,
                )
                if invalid_fields:
                    logger.warning(
                        f"WARNING({self.__class__.__name__})--------->>Invalid field names in request data: {invalid_fields}",
                    )
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid field names in request data",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_fields": invalid_fields,
                                "message": "Some field names are not valid for The Product Brand.",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if active_status:
                    is_valid, valid_choices = get_validated_choices_field(
                        choices_class=ActiveStatusChoices,
                        choices_value=active_status,
                    )

                    if not is_valid:
                        logger.warning(
                            f"WARNING({self.__class__.__name__})--------->>Invalid active_status: {active_status}",
                        )

                        # Warning Response if active status is not valid
                        return Response(
                            ErrorResponse(
                                status=status.HTTP_400_BAD_REQUEST,
                                type=ErrorType.WARNING,
                                message="Invalid active_status",
                                client=ResponseClient.DEVELOPER,
                                description={
                                    "active_status": f"Must be one of {', '.join(valid_choices)}",
                                    "info": "If you want to update active status provide correct choices 'active'or 'inactive'",
                                },
                            ).model_dump(),
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                invalid_relationship = []
                not_exist_relationship = []
                # check product relationship validity

                # Check product supplier relationship validity
                if category:
                    try:
                        object_id = int(category)
                        if object_id > 0:
                            if not self.category_model.objects.filter(
                                id=object_id
                            ).exists():
                                not_exist_relationship.append(
                                    {
                                        "category": object_id,
                                        "info": f"Category with id {object_id} not found",
                                    }
                                )
                    except ValueError:
                        invalid_relationship.append(
                            {
                                "category": category,
                                "info": "Invalid category id, category must be a positive integer",
                            },
                        )

                # Invalid Relationship Response
                if invalid_relationship:
                    logger.warning(
                        f"WARNING({self.__class__.__name__}):--------->> Invalid relationships: {invalid_relationship}",
                    )
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid relationships",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_relationships": invalid_relationship,
                                "info": "Check your relationships data with other objects",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Not exist relationship Response
                if not_exist_relationship:
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid relationship",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "not_exist_relationships": not_exist_relationship,
                                "info": "Check your relationships data with other objects",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if sub_category_name:
                    # Check if the category name already exists
                    if self.model_class.objects.filter(
                        sub_category_name=sub_category_name
                    ).exists():
                        logger.warning(
                            f"WARNING({self.__class__.__name__})----->>Sub-Category name already exists: {sub_category_name}",
                        )
                        # Unique object warning response
                        return Response(
                            ErrorResponse(
                                status=status.HTTP_400_BAD_REQUEST,
                                type=ErrorType.WARNING,
                                message=f"{self.model_class.__name__} name already exists",
                                client=ResponseClient.USER,
                                description={
                                    "sub_category_name": f"{sub_category_name}",
                                    "info": f"sub-category name '{sub_category_name}' already exists, try a different sub_category_name",
                                },
                            ).model_dump(),
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                try:
                    data = self.model_class.objects.get(id=id)
                    validated_data = self.serializer_class(
                        data,
                        data=request.data,
                        partial=partial,
                    )

                    if validated_data.is_valid():
                        updated_fields = list(request.data.keys())
                        validated_data.save()
                        return Response(
                            UpdateResponse(
                                status=status.HTTP_200_OK,
                                message=(
                                    f"{self.model_class.__name__} updated successfully"
                                    if not partial
                                    else f"{self.model_class.__name__} partially updated successfully"
                                ),
                                client=ResponseClient.USER,
                                details={
                                    "info": "Following fields are updated",
                                    "fields": updated_fields,
                                },
                                links=get_response_links(
                                    action="update", url_prefix=URL_PREFIX
                                ),
                            ).model_dump(),
                            status=status.HTTP_200_OK,
                        )
                    else:
                        # Log and respond with validation errors
                        logger.error(
                            f"ERROR({self.__class__.__name__}))----->>sub-category Update Serializer Error: {str(validated_data.errors)}",
                        )
                        # Error Response for data validation
                        return Response(
                            ErrorResponse(
                                status=status.HTTP_400_BAD_REQUEST,
                                type=ErrorType.WARNING,
                                message="Data Validation Error",
                                client=ResponseClient.DEVELOPER,
                                description={
                                    "errors": validated_data.errors,
                                    "info": "Some fields in the request data are invalid.",
                                },
                            ).model_dump(),
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except self.model_class.DoesNotExist:
                    return Response(
                        # Error Response for if product brand not found
                        ErrorResponse(
                            status=status.HTTP_404_NOT_FOUND,
                            type=ErrorType.WARNING,
                            message=f"{self.model_class.__name__} not found",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "id": id,
                                "info": f"No {self.model_class.__name__} found with the provided ID.",
                            },
                        ).model_dump(),
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                return Response(
                    ErrorResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        type=ErrorType.WARNING,
                        message="No data provided in the request",
                        client=ResponseClient.DEVELOPER,
                        description={
                            "info": "No data provided in the request, provide one or more valid necessary dta to update",
                        },
                    ).model_dump(),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            # Catch any unexpected errors
            logger.error(
                f"ERROR({self.__class__.__name__})----->>Error occurred while updating {MODEL_NAME}: {str(e)}",
            )

            # Return Response for any uneven errors
            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="A server-side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": f"An unexpected error occurred while updating {MODEL_NAME}",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<------------------------*** PRODUCT CATEGORY LIST API VIEW ***------------------------->>
@allowed_methods("GET")
class ListProductSubCategoryAPIView(APIView):
    """
    API endpoint to retrieve a list of all product categories.
    """

    # TODO:
    # Add permissions Class

    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = None

    def __init__(self, *args, **kwargs):
        self.model_class = SubCategory
        self.serializer_class = SubCategorySerializer
        self.filter_class = SubCategorySearchFilter
        super().__init__(*args, **kwargs)

    @extend_schema(
        summary=f"API endpoint for {MODEL_NAME}",
        description=f"This API endpoint is used to retrieve {MODEL_NAME} list",
        tags=[TAG_NAME],
        parameters=[
            ParameterAPIDocumentation.get_limit_parameter(),
            ParameterAPIDocumentation.get_offset_parameter(),
            ParameterAPIDocumentation.get_from_date_parameter(),
            ParameterAPIDocumentation.get_to_date_parameter(),
            ParameterAPIDocumentation.get_active_status_parameter(),
            ParameterAPIDocumentation.get_query_parameter(
                supported_fields="id,sub_category_name, category_name",
                example_value="tablet",
            ),
            ParameterAPIDocumentation.get_ordering_parameter(
                ordering_fields="id, sub_category_name, created_at, updated_at",
                example_value="-id",
            ),
            ParameterAPIDocumentation.get_field_list_parameter(
                fields_list="id,sub_category_name,category,parent_id,is_client_usable,sub_category_icon,active_status,description,created_at,updated_at",
                example_value="id,sub_category_name,category",
            ),
            ParameterAPIDocumentation.get_field_list_parameter(
                fields_list="category",
                example_value="1",
                field_name="category",
            ),
        ],
        responses={
            status.HTTP_200_OK: SuccessResponse,
            status.HTTP_400_BAD_REQUEST: ErrorResponse,
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorResponse,
        },
        examples=[
            ResponseAPIDocumentation.get_200_response(
                example={
                    "count": 100,
                    "limit": 10,
                    "offset": 0,
                    "next": "http://api.example.com/brand/list/?limit=10&offset=10",
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "created_at": "2025-02-28T20:08:40.434798Z",
                            "updated_at": "2025-03-01T03:53:11.823137Z",
                            "sub_category_name": "Capsule",
                            "parent_id": 0,
                            "sub_category_icon": "/media/product/sub_categories/medicine.png",
                            "is_client_usable": False,
                            "active_status": "active",
                            "description": "This is short but more amazing description",
                            "category": {
                                "id": 1,
                                "category_name": "Medicine",
                            },
                        },
                        {
                            "id": 2,
                            "created_at": "2025-03-01T04:18:27.273307Z",
                            "updated_at": "2025-03-01T04:18:27.273348Z",
                            "sub_category_name": "Tablet",
                            "parent_id": 0,
                            "sub_category_icon": "/media/product/sub_categories/medicine_1G0b9qp.png",
                            "is_client_usable": False,
                            "active_status": "active",
                            "description": "This is short but amazing description",
                            "category": {
                                "id": 1,
                                "category_name": "Medicine",
                            },
                        },
                    ],
                },
            ),
            ResponseAPIDocumentation.get_400_response(),
            ResponseAPIDocumentation.get_500_response(),
        ],
    )
    def get(self, request, *args, **kwargs):
        try:
            # Get all model field names for Category
            model_fields = get_model_fields(self.model_class)

            # Check query parameters validation
            check_query_params = get_valid_query_params(
                action="list",
                query_params=set(request.query_params.keys()),
                extended_fields=[
                    "category",
                ],
            )

            if check_query_params:
                if not check_query_params.get("is_valid", False):
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid query parameters",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_params": check_query_params.get(
                                    "invalid_params", None
                                ),
                                "allowed_prams": check_query_params.get(
                                    "allowed_params", None
                                ),
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            field_list = request.query_params.get("field_list", None)
            ordering = request.query_params.get("ordering", None)
            active_status = request.query_params.get("active_status", None)

            # Validate field_list against model_fields
            fields = []
            if field_list:
                fields, invalid_fields = get_validated_response_fields(
                    field_list=field_list,
                    model_fields=model_fields,
                )

                if invalid_fields:
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid fields in field_list parameter",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_fields": invalid_fields,
                                "info": "Provide Valid Field name that are exist in model",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Validate ordering against model_fields
            ordering_fields = []
            if ordering:
                ordering_fields, invalid_ordering_fields = (
                    get_validated_response_fields(
                        field_list=ordering,
                        model_fields=model_fields,
                        validation_type="ordering",
                    )
                )

                if invalid_ordering_fields:
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid fields in ordering parameter",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_fields": invalid_ordering_fields,
                                "info": "Provide Valid Field name that are exist in model",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            if active_status:
                is_valid, valid_choices = get_validated_choices_field(
                    choices_class=ActiveStatusChoices,
                    choices_value=active_status,
                )
                print("Valid Choices: ", valid_choices)

                if not is_valid:
                    logger.warning(
                        f"WARNING({self.__class__.__name__})--------->>Invalid active_status: {active_status}",
                    )

                    # Warning Response if active status is not valid
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid active_status query parameter",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "active_status": f"Must be one of {', '.join(valid_choices)}",
                                "info": "If you want to filter by active_status, provide one of the following values: active, inactive",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Retrieve all categories
            data = self.model_class.objects.all()
            data = self.filter_class(request.GET, queryset=data).qs

            # Apply ordering if specified
            if ordering:
                data = data.order_by(*ordering_fields)

            # serializer = CategorySerializer(categories, many=True)
            category_list = get_paginated_response(
                pagination_class=self.Pagination,
                serializer_class=self.serializer_class,
                queryset=data,
                request=request,
                view=self,
                fields=fields,
            )

            return Response(
                SuccessResponse(
                    status=status.HTTP_200_OK,
                    message=f"{self.model_class.__name__} list retrieved successfully",
                    client=ResponseClient.USER,
                    data=[category_list.data],
                    links=get_response_links(action="list", url_prefix=URL_PREFIX),
                ).model_dump(),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # Handle unexpected errors
            logger.error(
                f"ERROR({self.__class__.__name__})---------------->> Error occurred while retrieving {MODEL_NAME}: {str(e)}",
            )

            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="A server-side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": f"An unexpected error occurred while retrieving {MODEL_NAME}",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<---------------------*** PRODUCT SUB-CATEGORY DETAIL API VIEW ***--------------------->>
@allowed_methods("GET")
class RetrieveProductSubCategoryAPIView(APIView):
    """
    API endpoint to retrieve a specific product sub-category.
    """

    # TODO:
    # Add permissions Class

    def __init__(self, **kwargs):
        self.model_class = SubCategory
        self.serializer_class = SubCategorySerializer
        super().__init__(**kwargs)

    # API Documentation for sub-category details
    @extend_schema(
        summary=f"API endpoint for {MODEL_NAME} details",
        description=f"The API endpoint provides detailed information about a specific product {MODEL_NAME}",
        tags=[TAG_NAME],
        parameters=[
            ParameterAPIDocumentation.get_field_list_parameter(
                fields_list="id,sub_category_name,category,parent_id,is_client_usable,sub_category_icon,active_status,description,created_at,updated_at",
                example_value="id,sub_category_name,category",
            ),
        ],
        responses={
            # Response for the different status code
            status.HTTP_200_OK: SuccessResponse,
            status.HTTP_400_BAD_REQUEST: ErrorResponse,
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorResponse,
        },
        examples=[
            # Example for the different status codes Response
            ResponseAPIDocumentation.get_200_response(
                message=f"{MODEL_NAME} Retrieve Successfully",
                example={
                    "id": 1,
                    "sub_category_name": "Capsule",
                    "parent_id": 0,
                    "sub_category_icon": "/media/product/sub_categories/medicine.png",
                    "is_client_usable": False,
                    "active_status": "active",
                    "description": "This is short but more amazing description",
                    "category": {
                        "id": 1,
                        "category_name": "Medicine",
                    },
                    "created_at": "2025-02-28T20:08:40.434798Z",
                    "updated_at": "2025-03-01T03:53:11.823137Z",
                },
            ),
            ResponseAPIDocumentation.get_400_response(),
            ResponseAPIDocumentation.get_500_response(),
        ],
    )
    # * ---->> HTTP GET Method to retrieve
    def get(self, request, id, *args, **kwargs):
        try:
            # Get all model field names for this view
            model_fields = get_model_fields(self.model_class)

            # Check query parameters validation
            check_query_params = get_valid_query_params(
                action="details",
                query_params=set(request.query_params.keys()),
            )

            if check_query_params:
                if not check_query_params.get("is_valid", False):
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid query parameters",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "invalid_params": check_query_params.get(
                                    "invalid_params", None
                                ),
                                "allowed_prams": check_query_params.get(
                                    "allowed_params", None
                                ),
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            field_list = request.query_params.get("field_list", None)

            # Object Not found response logic
            if not self.model_class.objects.filter(id=id).exists():
                return Response(
                    ErrorResponse(
                        status=status.HTTP_404_NOT_FOUND,
                        type=ErrorType.WARNING,
                        message=f"{self.model_class.__name__} not found with the id {id}",
                        client=ResponseClient.DEVELOPER,
                        description={
                            "content_not_found": f"Product {self.model_class.__name__} with id {id} not found.",
                            "info": "Please check the id and try again.",
                        },
                    ).model_dump(),
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Validate field_list against model_fields
            fields = []
            if field_list:
                fields, invalid_fields = get_validated_response_fields(
                    field_list=field_list,
                    model_fields=model_fields,
                )

                # Invalid fields response logic
                if invalid_fields:
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Invalid fields in field_list parameter",
                            client=ResponseClient.DEVELOPER,
                            description={"invalid_fields": invalid_fields},
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Get The Data and retrieve
            data = self.model_class.objects.get(id=id)
            serializer = self.serializer_class(data, fields=fields)

            # Success Response Code
            return Response(
                SuccessResponse(
                    status=status.HTTP_200_OK,
                    message=f"{self.model_class.__name__} retrieved successfully",
                    client=ResponseClient.USER,
                    data=[serializer.data],
                    links=get_response_links(action="details", url_prefix=URL_PREFIX),
                ).model_dump(),
                status=status.HTTP_200_OK,
            )
        # Internal Server Error Response Code
        except Exception as e:
            # Handle unexpected errors
            logger.error(
                f"ERROR({self.__class__.__name__}):-------->>Error occurred while retrieving {MODEL_NAME}: {str(e)}",
            )

            # Unexpected error response
            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="A server-side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": f"An unexpected error occurred while retrieving {MODEL_NAME}",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<---------------------*** PRODUCT SUB-CATEGORY DELETE API VIEW ***--------------------->>
@allowed_methods("DELETE")
class DeleteProductSubCategoryAPIView(APIView):
    """
    API endpoint to delete a specific product sub-category.
    """

    def __init__(self, **kwargs):
        self.model_class = SubCategory
        self.product_model = Product
        super().__init__(**kwargs)

    # API Documentation for deleting a product brand
    @extend_schema(
        summary=f"API endpoint to delete a product {MODEL_NAME}",
        description=f"The {MODEL_NAME} Delete API endpoint allows the deletion of a specific product {MODEL_NAME} by its ID.",
        tags=[TAG_NAME],
        responses={
            status.HTTP_204_NO_CONTENT: NoContentResponse,
            status.HTTP_404_NOT_FOUND: ErrorResponse,
            status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorResponse,
        },
        examples=[
            ResponseAPIDocumentation.get_204_response(
                message=f"{MODEL_NAME} deleted successfully",
            ),
            ResponseAPIDocumentation.get_404_response(),
            ResponseAPIDocumentation.get_500_response(),
        ],
    )
    # * ---->> HTTP DELETE Method to delete
    def delete(self, request, id, *args, **kwargs):
        try:
            # Check sub-category has any relationship objects in product
            if self.product_model.objects.filter(sub_category=id).exists():
                return Response(
                    ErrorResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        type=ErrorType.WARNING,
                        message="Cannot delete a product sub-category that has associated products",
                        client=ResponseClient.DEVELOPER,
                        description={
                            "content_not_deleted": f"Product sub-category with id {id} has associated products",
                            "info": "Please delete the associated products before deleting the sub-category",
                        },
                    ).model_dump(),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Check if the brand exists
            object = self.model_class.objects.filter(id=id).first()
            if not object:
                return Response(
                    ErrorResponse(
                        status=status.HTTP_404_NOT_FOUND,
                        type=ErrorType.WARNING,
                        message=f"{self.model_class.__name__} not found",
                        client=ResponseClient.DEVELOPER,
                        description={
                            "content_not_found": f"{self.model_class.__name__} with id {id} not found.",
                            "info": f"Provide valid brand id to delete a specific {MODEL_NAME}",
                        },
                    ).model_dump(),
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Perform the deletion
            object.delete()

            # No Content Response Code (204)
            return Response(
                NoContentResponse(
                    status=status.HTTP_204_NO_CONTENT,
                    alternate_status=status.HTTP_200_OK,
                    message=f"{self.model_class.__name__} deleted successfully",
                    client=ResponseClient.USER,
                    description={
                        "hint": "Used 200 ok status code for the boyd content, as 204 has no body content",
                        "id": f"{self.model_class.__name__} with id {id} deleted successfully",
                    },
                ).model_dump(),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Internal Server Error Response Code
            logger.error(
                f"ERROR({self.__class__.__name__}):----->>Error occurred while deleting the {MODEL_NAME}: {str(e)}"
            )
            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="A server-side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": f"An unexpected error occurred while deleting {MODEL_NAME}",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
