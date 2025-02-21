from collections import OrderedDict
from math import ceil

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 20
    max_limit = 50

    def get_paginated_response(self, data):
        limit = int(self.request.query_params.get("limit", self.default_limit))
        offset = self.offset or 0
        count = self.count
        page_count = ceil(count / limit) if limit else 1

        return Response(
            OrderedDict(
                [
                    ("count", count),
                    ("limit", limit),
                    ("offset", offset),
                    ("page_count", page_count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ],
            ),
        )


def get_paginated_response(
    pagination_class,
    serializer_class,
    queryset,
    request,
    view,
    *args,
    **kwargs,
):
    # Extract limit and offset from request
    limit = request.query_params.get("limit")
    offset = request.query_params.get("offset")

    paginator = pagination_class()

    # Set limit and offset if provided
    if limit is not None:
        paginator.default_limit = int(limit)
    if offset is not None:
        paginator.offset = int(offset)

    page = paginator.paginate_queryset(queryset, request, view=view)

    # Pass fields argument only if it exists in kwargs
    serializer_kwargs = {
        "many": True,
    }
    if "fields" in kwargs:
        serializer_kwargs["fields"] = kwargs["fields"]

    if page is not None:
        serializer = serializer_class(page, **serializer_kwargs)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, **serializer_kwargs)
    return Response(data=serializer.data)
