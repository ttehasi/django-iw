import django_filters
from models.models import Campaign

class CampaignFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(
        field_name='created_at', 
        lookup_expr='gte',
        help_text="Фильтр по дате создания позднее даты (включительно), формат: YYYY-MM-DD"
    )
    created_before = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text="Фильтр по дате создания до даты (включительно), формат: YYYY-MM-DD"
    )

    class Meta:
        model = Campaign
        fields = []