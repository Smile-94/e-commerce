def get_valid_query_params(
    action: str,
    query_params: set,
    extended_fields: list[str] | None = None,
    *args,
    **kwargs,
):
    allowed_actions = ["list", "details"]
    if action not in allowed_actions:
        raise ValueError(f"Invalid action: {action}. Only allowed: {allowed_actions}")

    if action == "list":
        allowed_query_params = {
            "limit",
            "offset",
            "field_list",
            "ordering",
            "query",
            "to_date",
            "active_status",
            "from_date",
        }
        if extended_fields:
            allowed_query_params.update(set(extended_fields))

        invalid_params = [
            field for field in query_params if field not in allowed_query_params
        ]

        if invalid_params:
            return {
                "allowed_params": allowed_query_params,
                "invalid_params": invalid_params,
                "is_valid": False,
            }
        return {"allowed_params": allowed_query_params, "is_valid": True}

    if action == "details":
        # Default allowed params
        allowed_query_params = {"field_list"}

        # # Allow all params if kwargs.get("other", False) is True
        # if kwargs.get("other", False):
        #     return {"allowed_params": "All", "is_valid": True}

        if extended_fields:
            allowed_query_params.update(set(extended_fields))
        # Validate against allowed_query_params
        invalid_params = [
            field for field in query_params if field not in allowed_query_params
        ]

        if invalid_params:
            return {
                "allowed_params": allowed_query_params,
                "invalid_params": invalid_params,
                "is_valid": False,
            }
        return {"allowed_params": allowed_query_params, "is_valid": True}
