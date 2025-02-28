from typing import Any

# Import Choices
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db.models import Field, Model, TextChoices
from loguru import logger


# This function is used to get the model fields
def get_model_fields(model_class: type[Model], *args, **kwargs) -> list[str]:
    """
    Returns a list of field names for the given Django model class.

    Args:
        model_class (type[Model]): The Django model class to get field names for.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        list[str]: A list of field names for the given Django model class.

    Raises:
        TypeError: If the provided class is not a Django model.
        FieldError: If there is an error retrieving fields for the model.
        Exception: If an unexpected error occurs.
    """
    try:
        # Check if the provided class is a Django model
        if not isinstance(model_class, type) or not issubclass(model_class, Model):
            logger.warning(
                f"WARNING(get_model_fields):-->> {model_class} is not a django model"
            )
            raise TypeError("Provided class is not a Django model.")

        # Get and return field names
        return [
            field.name
            for field in model_class._meta.get_fields()
            if isinstance(field, Field)
        ]

    except TypeError as e:
        logger.error(
            f"ERROR(get_model_fields):------>> Error in  get model fields: {model_class.__name__}, {e}"
        )
        raise e  # Re-raise the TypeError with a meaningful message

    except FieldError as e:
        logger.error(
            f"ERROR(get_model_fields):------>> Error in get model fields: {model_class.__name__}, {e}"
        )
        raise FieldError(
            f"Error retrieving fields for model {model_class.__name__}: {str(e)}"
        )

    except Exception as e:
        logger.error(
            f"ERROR(get_model_fields):------>> Error in get model fields: {model_class.__name__}, {e}"
        )
        raise Exception(f"An unexpected error occurred: {str(e)}")


# This function is used to validate the request data fields
def get_validated_request_fields(
    model_class: type[Model],
    request_data: dict[str, Any],
    extended_fields: list[str] | None = None,
    *args,
    **kwargs,
) -> Any:
    """
    Validates and extracts field names from the provided request data.

    Args:
        model_class (type[Model]): The Django model class to validate field names against.
        request_data (dict[str, Any]): The request data containing field names.
        extended_fields (list[str] | None, optional): Additional fields to be included in validation. Defaults to None.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Any: A list of invalid field names if any, or a dictionary containing an error message if validation fails.

    Raises:
        FieldDoesNotExist: If a model field does not exist.
        Exception: If an unexpected error occurs during validation.
    """
    try:
        # Get valid field names for the model
        valid_field_names = [field.name for field in model_class._meta.fields]

        if extended_fields:
            valid_field_names.extend(
                extended_fields
            )  # Add extended fields to the valid list

        # Validate field names in request data
        invalid_fields = [
            field for field in request_data.keys() if field not in valid_field_names
        ]

        return invalid_fields

    except FieldDoesNotExist as e:
        # Specific error handling if model field does not exist
        logger.error(f"ERROR(get_validated_request_fields):--->> {e}")
        return {"error": "Model field does not exist, check your model definition."}

    except Exception as e:
        # General error handling
        logger.error(f"ERROR(get_validated_request_fields):---->> {e}")
        return {"error": f"An unexpected error occurred: {str(e)}"}


# This function is used to validate request field in request data
def get_validated_response_fields(
    field_list: str,
    model_fields: list,
    validation_type: str = "field_list",
    extended_fields: list[str] | None = None,
    *args,
    **kwargs,
) -> tuple:
    """
    Validates and extracts field names from the provided field list.

    Args:
        field_list (str): A comma-separated list of field names.
        model_fields (list): A list of valid field names for the model.
        validation_type (str, optional): The type of validation to be performed. Defaults to "field_list".
        extended_fields (list[str] | None, optional): Additional fields to be included in validation. Defaults to None.

    Returns:
        tuple: A tuple containing a list of valid field names and a list of invalid field names.

    Raises:
        ValueError: If the field_list is an empty or whitespace-only string.
        Exception: If an unexpected error occurs during validation.
    """
    if not field_list.strip():
        raise ValueError("field_list cannot be an empty or whitespace-only string.")

    try:
        # Extract fields and remove extra spaces
        fields = [field.strip() for field in field_list.split(",") if field.strip()]

        # Separate valid and invalid fields
        valid_fields = []
        invalid_fields = []

        for field in fields:
            # If ordering, strip '-' for validation, but keep it in the valid list if present
            clean_field = field.lstrip("-") if validation_type == "ordering" else field
            if clean_field in model_fields:
                valid_fields.append(field)  # Keep original field with '-' if present
            else:
                invalid_fields.append(field)

        if extended_fields:
            valid_fields.extend(
                extended_fields
            )  # Add extended fields to the valid list

    except Exception as e:
        logger.error(f"ERROR(get_validated_response_fields):----> {e}")

        raise ValueError(f"ERROR(get_validated_response_fields):---->> {e}")

    return valid_fields, invalid_fields


# This function will return all the required fields in request data
def get_missing_required_fields(
    model_class: type[Model],
    request_data: dict[str, Any],
    extended_required_fields: list[str] | None = None,
    *args,
    **kwargs,
) -> Any:
    """
    Validate that the required fields are present in the data.
    :param data: Dictionary of request data
    :param required_fields: List of field names that are required
    :return: Dictionary of missing fields with error messages if any field is missing, else an empty dictionary
    """
    try:
        # Get all required fields from the model
        required_fields = [
            field.name
            for field in model_class._meta.fields
            if not field.blank and not field.null
        ]

        # Extend required fields if additional ones are provided
        if extended_required_fields:
            required_fields.extend(extended_required_fields)

        # Find missing required fields in the request data
        missing_fields = [
            field for field in required_fields if field not in request_data
        ]

        empty_fields = [
            field
            for field in required_fields
            if field in request_data and request_data[field] in [None, ""]
        ]

        return missing_fields, empty_fields

    except Exception as e:
        logger.error(f"ERROR(get_missing_required_fields): {str(e)}")

        raise ValueError(f"An error occurred while validating required fields: {e}")


# This function is used to validate choices field in django
def get_validated_choices_field(
    choices_class: type[TextChoices],
    choices_value: str,
    *args,
    **kwargs,
) -> tuple:
    """
    Validates the provided status against the ActiveStatusChoice values.
    Returns a tuple with a boolean indicating validity and the list of valid choices.
    """
    valid_choices = [choice[0] for choice in choices_class.choices]

    is_valid = False
    if choices_value in valid_choices:
        is_valid = True

        return is_valid, valid_choices
    else:
        return is_valid, valid_choices
