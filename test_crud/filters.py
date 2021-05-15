import django_filters
from django_filters import rest_framework as filters
from .models import logs


class logsFilter(filters.FilterSet):
    class Meta:
        model = logs
        fields = {'has_mutation', 'timestamp'}