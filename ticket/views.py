from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView

from .forms import ProblemForm
from .models import Problem, Partnyor
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django_filters.views import FilterView

from django_filters import FilterSet
from ticket.models import Problem, Compleks, Company, Partnyor as partnyorModel


class ProblemListView(ListView, FilterView):
    model = Problem
    template_name = 'problem.html'

class ProblemDetail(DetailView):
    model = Problem
    template_name = "problems/problem_detail.html"

class ProblemUpdateView(UpdateView):
    model = Problem
    fields = ('name', 'created', 'status', 'creatorId')
    template_name = 'problems/problemEdit.html'



class ProblemDelete(DeleteView):
    model = Problem
    template_name = 'problems/problemDelete.html'
    success_url = reverse_lazy('problem_list')

class ProblemCreateView(CreateView):
    model = Problem
    template_name = 'problems/problemCreate.html'
    fields = ('name', 'created', 'status', 'creatorId')

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

def Partnyor(request):
    labels = []
    data = []

    queryset = partnyorModel.objects.order_by('-age')[:3]
    for part in queryset:
        labels.append(part.login)
        data.append(part.age)
    return render(request, 'partnyor.html', {
        'labels': labels,
        'data': data
        })










