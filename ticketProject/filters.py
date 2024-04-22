from decimal import Decimal

from django.db.models import Q
from django.db.models.functions import math
from django.forms import TextInput
import django_filters

from ticket.models import Problem


class ProblemFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label="")
    name = django_filters.CharFilter(label="", lookup_expr="istartswith")
    # category = django_filters.CharFilter(label="", lookup_expr="istartswith")
    # price = django_filters.NumberFilter(label="", method="filter_decimal")
    # cost = django_filters.NumberFilter(label="", method="filter_decimal")
    status = django_filters.ChoiceFilter(label="", choices=Problem.Status.choices)

    class Meta:
        model = Problem
        fields = ["id", "name",   "status"]
        # fields = ["id", "name", "category", "price", "cost", "status"]

    def filter_decimal(self, queryset, name, value):
        # For price and cost, filter based on
        # the following property:
        # value <= result < floor(value) + 1

        lower_bound = "__".join([name, "gte"])
        upper_bound = "__".join([name, "lt"])

        upper_value = math.floor(value) + Decimal(1)

        return queryset.filter(**{lower_bound: value,
                                  upper_bound: upper_value})