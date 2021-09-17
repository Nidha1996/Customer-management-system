from django.db.models import fields
import django_filters
from django_filters import DateFilter,CharFilter

from accounts.models import *

class Orderfilter(django_filters.FilterSet):
    start_date=DateFilter(field_name="data_created",lookup_expr="gte",label="Date from")
    end_date=DateFilter(field_name="data_created",lookup_expr="lte",label="Date to")
    note=CharFilter(field_name="note",lookup_expr="contains")
    class Meta:
        model =Order
        fields="__all__"
        exclude=['customer','data_created']