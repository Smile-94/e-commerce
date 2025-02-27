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
from apps.products.filters.brand_filter import BrandSearchFilter

# Models Import
from apps.products.models.brand_model import Brand

# Import Serializer
from apps.products.serializers.brand_serializer import (
    BrandSerializer,
    BrandUpdateSerializer,
)

# API TAGS Name
MODEL_NAME = "Brand"
URL_PREFIX = "brand"
TAG_NAME = "Brand [v1]"


# * <<---------------------*** CREATE PRODUCT BRAND API VIEW ***--------------------->>
@allowed_methods("POST")
class CreateProductBrandAPIView(APIView):
    """
    API endpoint to create a new product Brand.
    """

    # TODO:
    # Add permissions Class

    def __init__(self, *args, **kwargs):
        self.model_class = Brand
        self.serializer_class = BrandSerializer
        super().__init__(*args, **kwargs)

    # API documentation
    @extend_schema(
        summary=f"API endpoint for creating product {MODEL_NAME}",
        description=f"Provide all necessary fields and values to create product {MODEL_NAME}",
        tags=[TAG_NAME],
        responses={
            "201": SuccessResponse,
            "400": ErrorResponse,
            "500": ErrorResponse,
        },
        examples=[
            ResponseAPIDocumentation.get_201_response(
                example={
                    "id": 1,
                    "brand_name": "Care-Box",
                    "origin_country": "Bangladesh",
                    "web_url": "https://www.care-box.com",
                    "brand_logo": "/brand/brand.jpg",
                    "contact_number": "+8801981701810",
                    "brand_email": "my@care-box.com",
                    "description": "This category contains medicines.",
                    "active_status": "active",
                    "created_at": "2024-10-29",
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
                brand_name = request.data.get("brand_name", None)
                active_status = request.data.get("active_status", None)

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
                if not brand_name:
                    logger.warning(
                        f"WARNING({self.__class__.__name__}):--------->> brand_name is required in request data."
                    )

                    # Return The required fields missing errors
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message="Brand Name is required",
                            client=ResponseClient.DEVELOPER,
                            description={
                                "brand_name": "brand_name missing",
                                "info": "'brand_name' is required to create new brand object",
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

                # Check the product name is exist or not, if not exist then create a new brand object
                if not self.model_class.objects.filter(brand_name=brand_name).exists():
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
                            f"ERROR({self.__class__.__name__}): brand create serializer error {serializer.errors}",
                        )

                        # Return Serializers Error Response
                        return Response(
                            ErrorResponse(
                                status=status.HTTP_400_BAD_REQUEST,
                                type=ErrorType.ERROR,
                                message="Data Validation Error",
                                client=ResponseClient.DEVELOPER,
                                description={"errors": serializer.errors},
                            ).model_dump(),
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                else:
                    return Response(
                        ErrorResponse(
                            status=status.HTTP_400_BAD_REQUEST,
                            type=ErrorType.WARNING,
                            message=f"{self.model_class.__name__} name already exists",
                            client=ResponseClient.USER,
                            description={
                                "brand_name": f"{request.data['brand_name']}",
                                "info": f"Brand name '{request.data['brand_name']}' already exists, try a different brand_name",
                            },
                        ).model_dump(),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                return Response(
                    ErrorResponse(
                        status=status.HTTP_400_BAD_REQUEST,
                        type=ErrorType.WARNING,
                        message="No Data Provided, Please provide payload data",
                        client=ResponseClient.DEVELOPER,
                        description={
                            "brand_name": "int, This field is required",
                            "origin_country": "str, This field is not required.",
                            "web_url": "url, optional",
                            "brand_logo": "ImageField, optional",
                            "contact_number": "str, optional",
                            "brand_email": "str, optional",
                            "active_status": "choice, optional, default='active'",
                            "description": "str, optional",
                        },
                    ).model_dump(),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            logger.error(
                f"----->>Error occurred while creating product Brand: {str(e)}",
            )
            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="An server side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": "An unexpected error occurred while creating brand",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<---------------------*** UPDATE PRODUCT BRAND API VIEW ***--------------------->>
@allowed_methods("PUT", "PATCH")
class UpdateProductBrandAPIView(APIView):
    """
    API endpoint to update an existing product category.
    """

    # TODO:
    # Add permissions Class

    def __init__(self, *args, **kwargs):
        self.model_class = Brand
        self.serializer_class = BrandUpdateSerializer
        super().__init__(*args, **kwargs)

    # Update Product Category API Documentation.
    @extend_schema(
        summary=f"API endpoint for updating a product {MODEL_NAME}",
        description=f"Provide all necessary fields and values to update a product {MODEL_NAME}",
        tags=[TAG_NAME],
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
                    "fields": ["brand_name", "brand_icon"],
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
        request=BrandSerializer,
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
                    "fields": ["category_name", "category_icon"],
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
            active_status = request.data.get("active_status", None)
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
            # Check if the category exists
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
                        f"ERROR({self.__class__.__name__}))----->>Brand Update Serializer Error: {str(validated_data.errors)}",
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

        except Exception as e:
            # Catch any unexpected errors
            logger.error(
                f"ERROR({self.__class__.__name__})----->>Error occurred while updating brand: {str(e)}",
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
                        "info": "An unexpected error occurred while creating brand",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<------------------------*** PRODUCT BRAND LIST API VIEW ***------------------------->>
@allowed_methods("GET")
class ListProductBrandAPIView(APIView):
    """
    API endpoint to retrieve a list of all product Brand.
    """

    # TODO:
    # Add permissions Class

    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = None

    def __init__(self, *args, **kwargs):
        self.model_class = Brand
        self.serializer_class = BrandSerializer
        self.filter_class = BrandSearchFilter
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
                supported_fields="id, brand_name, origin_country, contact_number, brand_email",
                example_value="care-box",
            ),
            ParameterAPIDocumentation.get_ordering_parameter(
                ordering_fields="id, brand_name, origin_country",
                example_value="-id",
            ),
            ParameterAPIDocumentation.get_field_list_parameter(
                fields_list="id,brand_name,origin_country,contact_number,brand_email,brand_logo,active_status,created_at,updated_at and description",
                example_value="id, brand_name, origin_country, contact_number,",
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
                            "id": 4,
                            "created_at": "2025-02-25T18:38:25.877080Z",
                            "updated_at": "2025-02-25T18:38:25.877140Z",
                            "brand_name": "Square",
                            "origin_country": "Bangladesh",
                            "brand_logo": "/media/product/brands/bd_beauty_glamours_Ka2ngaB.jpeg",
                            "web_url": "https://wwwe.intel.com",
                            "contact_number": "+8801920252203",
                            "brand_email": "intel@intel.com",
                            "active_status": "active",
                            "description": "This is short but amazing description",
                        },
                        {
                            "id": 3,
                            "created_at": "2025-02-25T18:35:10.267453Z",
                            "updated_at": "2025-02-25T18:35:10.267609Z",
                            "brand_name": "ASUS",
                            "origin_country": "Bangladesh",
                            "brand_logo": "/media/product/brands/brand.png",
                            "web_url": "https://wwwe.intel.com",
                            "contact_number": "+8801920252203",
                            "brand_email": "intel@intel.com",
                            "active_status": "active",
                            "description": "This is short but amazing description",
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
                action="list", query_params=set(request.query_params.keys())
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
                f"ERROR({self.__class__.__name__})---------------->> Error occurred while retrieving brand: {str(e)}",
            )

            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="A server-side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": "An unexpected error occurred while creating brand",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<---------------------*** PRODUCT BRAND DETAIL API VIEW ***--------------------->>
@allowed_methods("GET")
class RetrieveProductBrandAPIView(APIView):
    """
    API endpoint to retrieve a specific product brand.
    """

    # TODO:
    # Add permissions Class

    def __init__(self, **kwargs):
        self.model_class = Brand
        self.serializer_class = BrandSerializer
        super().__init__(**kwargs)

    # API Documentation for sub-category details
    @extend_schema(
        summary=f"API endpoint for {MODEL_NAME} details",
        description=f"The API endpoint provides detailed information about a specific product {MODEL_NAME}",
        tags=[TAG_NAME],
        parameters=[
            ParameterAPIDocumentation.get_field_list_parameter(
                fields_list="id,brand_name,origin_country,contact_number,brand_email,brand_logo,active_status,created_at,updated_at and description",
                example_value="id, brand_name,",
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
                    "brand_name": "Intel",
                    "origin_country": "Bangladesh",
                    "brand_logo": "Brand/icon.jpg",
                    "description": "This is short but amazing description",
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
                f"ERROR({self.__class__.__name__}):-------->>Error occurred while retrieving brand: {str(e)}",
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
                        "info": "An unexpected error occurred while creating brand",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# * <<---------------------*** PRODUCT BRAND DELETE API VIEW ***--------------------->>
@allowed_methods("DELETE")
class DeleteProductBrandAPIView(APIView):
    """
    API endpoint to delete a specific product brand.
    """

    def __init__(self, **kwargs):
        self.model_class = Brand
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
                            "info": "Provide valid brand id to delete a specific brand",
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
                f"ERROR({self.__class__.__name__}):----->>Error occurred while deleting the brand: {str(e)}"
            )
            return Response(
                ErrorResponse(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    type=ErrorType.ERROR,
                    message="A server-side error occurred while processing your request",
                    client=ResponseClient.DEVELOPER,
                    description={
                        "error": str(e),
                        "info": "An unexpected error occurred while creating brand",
                        "message": "Please Contact with the support, we will get back to you soon",
                    },
                ).model_dump(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
