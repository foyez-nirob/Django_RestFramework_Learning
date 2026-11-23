import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    dept = django_filters.CharFilter(field_name='dept', lookup_expr='icontains')
    id = django_filters.RangeFilter(field_name='id', lookup_expr='exact')
    # filter by employee id range
    id_min = django_filters.CharFilter(method='filter_id_by_range', label='Minimum ID')
    id_max = django_filters.CharFilter(method='filter_id_by_range', label='Maximum ID')

    class Meta:
        model = Employee
        fields = ['name', 'dept', 'id']

    def filter_id_by_range(self, queryset, name, value):
        if name == 'id_min':
            queryset = queryset.filter(id__gte=value)
        elif name == 'id_max':
            queryset = queryset.filter(id__lte=value)
        return queryset
