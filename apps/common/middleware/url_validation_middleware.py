# custom_middleware.py
from django.http import JsonResponse
from django.urls import Resolver404, resolve
from rest_framework import status

from apps.common.dataclass.response_dataclass import (
    InvalidUrlResponse,
    ResponseClient,
)


class UrlValidationMiddleware:
    """
    Middleware to check if the request URL exists.
    If not, returns a 404 Page Not Found response using InvalidUrlResponse model.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Attempt to resolve the URL path
            resolve(request.path)
        except Resolver404:
            # Create the response using the InvalidUrlResponse model
            error_response = InvalidUrlResponse(
                status=status.HTTP_404_NOT_FOUND,
                message="404 Page Not Found",
                client=ResponseClient.DEVELOPER,  # Specify client or adjust as necessary
                description={"info": "The requested URL was not found on the server."},
            )
            return JsonResponse(
                error_response.model_dump(),
                status=status.HTTP_404_NOT_FOUND,
            )

        # If the URL is valid, continue processing the request
        response = self.get_response(request)
        return response
