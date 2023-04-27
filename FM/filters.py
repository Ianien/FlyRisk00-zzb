import django_filters
from .models import FlyTask


class FlyTaskFilter(django_filters.rest_framework.FilterSet):
    found_time = django_filters.DateFromToRangeFilter()
    alter_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = FlyTask
        fields = []
