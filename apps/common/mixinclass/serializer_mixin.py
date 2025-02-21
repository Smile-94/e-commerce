class FilterFieldMixin:
    """
    A mixin for filtering serializer fields based on the provided fields list.
    """

    def __init__(self, model_field, *args, **kwargs):
        self.model_field = model_field
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        # If 'fields' is specified, filter the serializer fields
        if fields:
            # Ensure fields is treated as a string
            if isinstance(fields, list):
                allowed_fields = {field.strip() for field in fields}

            else:
                # Split the fields string into a list and strip whitespace
                allowed_fields = {field.strip() for field in fields.split(",")}

            existing_fields = set(self.model_field.keys())

            # Remove fields that are not in the allowed list
            for field_name in existing_fields - allowed_fields:
                self.model_field.pop(field_name)

            self.allowed_fields = set(allowed_fields)
