from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.utils import timezone
from datetime import datetime
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django_filters.views import FilterView
from django_filters import FilterSet
from ticket.models import Problem, Compleks, Company, Partnyor as partnyorModel, Partnyor
from django.contrib.auth.views import LoginView
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class ProblemListView(ListView, FilterView):
    model = Problem
    template_name = 'problems/problem.html'

class ProblemDetail(DetailView):
    model = Problem
    template_name = "problems/problem_detail.html"

@login_required(login_url='/accounts/login/')
def edit(request, pk):
    post = get_object_or_404(Problem, pk=pk)
    try:
        problem = Problem.objects.get(id=pk)
        if request.method == "POST":
            problem.name = request.POST.get("name")
            problem.created = timezone.now()
            problem.status = request.POST.get("status")
            problem.creatorId = request.user
            problem.save()
            return HttpResponseRedirect("../.")
        else:
            return render(request, "problems/problemEdit.html", {"problem": problem})
    except Problem.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def ProblemNew(request):
    try:
        if request.method == "POST":
            problem = Problem()
            problem.name = request.POST.get("name")
            problem.created = timezone.now()
            problem.status = request.POST.get("status")
            problem.creatorId = request.user
            problem.save()
            return HttpResponseRedirect("../problems")
        else:
            return render(request, "problems/problemCreate.html")
    except Problem.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

class ProblemDelete(DeleteView):
    model = Problem
    template_name = 'problems/problemDelete.html'
    success_url = reverse_lazy('problem_list')

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

    partnyor_data = Partnyor.objects.all()

    return render(request, 'partnyor.html',  {'partnyor_data': partnyor_data})

def pie_chart(request):
    labels = []
    data = []

    queryset = Partnyor.objects.order_by('-age')[:5]
    for partnyorModel in queryset:
        labels.append(partnyorModel.fio)
        data.append(partnyorModel.age)

    return render(request, 'partnyor.html', {
        'labels': labels,
        'data': data,
    })


def ticket_class_view(request):
    dataset = Partnyor.objects \
        .values('age') \
        .annotate(status_count=Count('age', filter=Q(status=1)),
                  not_status_count=Count('age', filter=Q(status=0))) \
        .order_by('age')
    return render(request, 'chart.html', {'dataset': dataset})


def chart_view(request):
    # Получаем данные из модели
    chart_data = Company.objects.annotate(month=ExtractMonth('created')).values('month').annotate(count=Count('id'))

    # Разделяем данные на месяцы и количество записей
    months = [data['month'] for data in chart_data]
    counts = [data['count'] for data in chart_data]

    # Контекст для передачи данных в шаблон
    context = {
        'months': json.dumps(months),
        'counts': json.dumps(counts),
    }

    return render(request, 'chart.html', context)

def ticket_chart(request):
    # Получаем данные для графика
    ticket_counts = Problem.objects.values('status').annotate(total=Count('status'))

    # Формируем данные для передачи в шаблон
    chart_data = {
        'labels': [item['status'] for item in ticket_counts],
        'data': [item['total'] for item in ticket_counts],
    }

    return render(request, 'ticket_chart.html', {'chart_data': chart_data})