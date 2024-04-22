from django.shortcuts import render
from django.views.generic import ListView
from django_filters.views import FilterView

from django_filters import FilterSet
from ticket.models import Problem, Compleks, Company, Partnyor as partnyorModel


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
    model = partnyorModel
    template_name = 'partnyor1.html'

def chart_view(request):
    labels = []
    data = []

    queryset = partnyorModel.objects.order_by('-age')[:5]
    for part in queryset:
        labels.append(part.login)
        data.append(part.age)
    return render(request, 'partyor.html', {
        'labels': labels,
        'data': data
    })