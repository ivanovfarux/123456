from django.shortcuts import render
from django.views.generic import ListView
from django_filters.views import FilterView

from django_filters import FilterSet
from ticket.models import Problem, Compleks, Company, Partnyor


class ProblemListView(ListView, FilterView):
    model = Problem
    template_name = 'problem.html'



class CompleksFilter(FilterSet):
    class Meta:
        model = Compleks
        fields = {"name": ["exact", "contains"], "status": ["exact"]}


class CompleksListView(ListView, FilterView):
    model = Compleks
    template_name = 'compleks.html'

    filterset_class = CompleksFilter

class CompanyListView(ListView, FilterView):
    model = Company
    template_name = 'company.html'

class PartnyorListView(ListView, FilterView):
    model = Partnyor
    template_name = 'partnyor.html'

def index(request):
    labels = []
    data = []
    queryset = Partnyor.objects.order_by('-age')[:5]
    for part in queryset:
        labels.append(part.fio)
        data.append(part.age)
    return render(request, 'partyor.html', {
        'labels': labels,
        'data': data
    })