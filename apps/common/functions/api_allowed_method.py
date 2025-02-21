from functools import wraps
from typing import Any

from django.http import JsonResponse

from apps.common.dataclass.response_dataclass import (
    ErrorResponse,
    ErrorType,
    ResponseClient,
)


def allowed_methods(*methods) -> Any:
    """
    A class decorator to enforce allowed HTTP methods on Django views.

    Usage:
        @allowed_methods('POST')
        class MyView(View):
            ...
    """

    def decorator(cls):
        # Store the original dispatch method of the class
        original_dispatch = cls.dispatch

        # Wrap the dispatch method to check the request method
        @wraps(original_dispatch)
        def new_dispatch(self, request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse(
                    ErrorResponse(
                        status=405,
                        type=ErrorType.WARNING,
                        message=f"This field only support {methods}",
                        client=ResponseClient.DEVELOPER,
                        description={
                            "warning": "Use appropriate method to send request"
                        },
                    ).model_dump(),
                    status=405,
                )
            return original_dispatch(self, request, *args, **kwargs)

        # Replace the dispatch method with the new one
        cls.dispatch = new_dispatch
        return cls

    return decorator
