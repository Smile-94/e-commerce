import datetime

from django.db.models import Model


def get_generated_custom_id(
    id_prefix: str,
    field: str,
    model_class: type[Model],
    *args,
    **kwargs,
) -> str:
    """
    Generates a custom order place ID with a prefix, date, and incremented counter.

    Args:
        id_prefix (str): The prefix to prepend to the ID (e.g., 'INV').
        field (str): The model field to order by and extract the last counter value.
        model_class (Type[Model]): The Django model class.

    Returns:
        str: The generated custom order ID.

    Raises:
        ValueError: If the specified field does not exist in the model.
    """
    # Ensure the model class contains the specified field
    if not hasattr(model_class, field):
        raise ValueError(
            f"The field '{field}' does not exist in the model '{model_class.__name__}'."
        )

    current_date = datetime.date.today()
    formatted_date = current_date.strftime("%d%m%y")

    # Fetch the latest ID that matches the current prefix and date
    latest_instance = (
        model_class.objects.filter(
            **{f"{field}__startswith": f"{id_prefix}{formatted_date}"}
        )
        .order_by(f"-{field}")  # Order by the field in descending order
        .first()
    )

    # Extract the last counter and increment, or start with 1 if none exist
    if latest_instance:
        latest_field_value = getattr(latest_instance, field, "")
        try:
            # Extract the last 4 digits as the counter
            previous_counter = int(latest_field_value[-4:])
            new_counter = (
                previous_counter + 1
            ) % 10000  # Increment and reset if > 9999
        except ValueError:
            new_counter = 1  # Fallback if the latest ID's counter isn't a valid number
    else:
        new_counter = 1

    # Ensure the counter is always four digits with leading zeros
    formatted_counter = str(new_counter).zfill(4)

    # Construct the new ID
    new_id = f"{id_prefix}{formatted_date}{formatted_counter}"
    return new_id
