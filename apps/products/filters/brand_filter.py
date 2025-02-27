import datetime

import django_filters
from django.db.models import Q
from django.utils import timezone

# Models
from apps.products.models.brand_model import Brand


# * <<---------------------------*** Product Brand Search Filter ***---------------------------------->>
class BrandSearchFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method="search", label="Search")
    from_date = django_filters.DateFilter(
        lookup_expr="gte",
        label="From Date",
    )
    to_date = django_filters.DateFilter(lookup_expr="lte", label="To Date")
    active_status = django_filters.CharFilter(
        field_name="active_status", label="Active Status"
    )

    class Meta:
        model = Brand
        fields = [
            "query",
        ]

    def search(self, queryset, name, value):
        try:
            # Apply the `id` filter only if `value` is numeric
            if value.isnumeric():
                filters = Q(id__exact=value)
            else:
                brand_name_result = queryset.filter(
                    brand_name__istartswith=value
                ).distinct()
                if brand_name_result.exists():
                    return brand_name_result

                else:
                    filters = (
                        Q(brand_name__icontains=value)
                        | Q(origin_country__icontains=value)
                        | Q(contact_number__icontains=value)
                        | Q(brand_email__icontains=value)
                    )

                return queryset.filter(filters).distinct()

        except ValueError:
            return queryset.filter(brand_name__icontains=value)

    def filter_queryset(self, queryset):
        self.from_date = self.data.get("from_date", None)
        self.to_date = self.data.get("to_date", None)
        self.active_status = self.data.get("active_status", None)
        search_value = self.data.get("query", None)

        # Convert date strings to datetime objects
        if self.from_date:
            self.from_date = timezone.make_aware(
                datetime.datetime.strptime(self.from_date, "%Y-%m-%d")
            )
        if self.to_date:
            self.to_date = timezone.make_aware(
                datetime.datetime.strptime(self.to_date, "%Y-%m-%d")
            ) + timezone.timedelta(
                days=1
            )  # Include the entire to_date

        # Apply active_status filter if provided
        if self.active_status is not None:  # None check to avoid issues with booleans
            queryset = queryset.filter(active_status=self.active_status)

        # Apply date range filters
        if self.from_date and self.to_date:
            queryset = queryset.filter(
                Q(created_at__gte=self.from_date) & Q(created_at__lt=self.to_date)
            )
        elif self.from_date:
            queryset = queryset.filter(created_at__gte=self.from_date)
        elif self.to_date:
            queryset = queryset.filter(created_at__lt=self.to_date)

        # Apply search filter if query is provided
        if search_value:
            queryset = self.search(queryset, "query", search_value)

        return queryset
