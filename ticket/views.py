from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django_filters.views import FilterView
from django_filters import FilterSet
from rest_framework import viewsets
from rest_framework.response import Response

from ticket.models import Problem, Compleks, Company, Partnyor as partnyorModel, Partnyor, Ticket, Duty
from django.contrib.auth.views import LoginView
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from ticket.serializer import ProblemSerializer, DutySerializer


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class ProblemViewSet(viewsets.ViewSet):
    def list(self, request):
        stu = Problem.objects.all()
        serializer = ProblemSerializer(stu, many=True)
        return Response(serializer.data)

class DutyViewSet(viewsets.ViewSet):
    def list(self, request):
        duty = Duty.objects.all()
        serializer = DutySerializer(duty, many=True)
        return Response(serializer.data)

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
            problem.createDate = timezone.now()
            problem.status = request.POST.get("status")
            problem.author = request.user
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
            problem.createDate = timezone.now()
            problem.status = request.POST.get("status")
            problem.author = request.user
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

class CompanyListView(ListView, FilterView):
    model = Company
    template_name = 'company/company.html'


class CompanyDetail(DetailView):
    model = Company
    template_name = "company/company_detail.html"

class CompanyDelete(DeleteView):
    model = Company
    template_name = 'company/companyDelete.html'
    success_url = reverse_lazy('company_list')

@login_required(login_url='/accounts/login/')
def Companyedit(request, pk):
    post = get_object_or_404(Company, pk=pk)
    try:
        company = Company.objects.get(id=pk)
        if request.method == "POST":
            company.name = request.POST.get("name")
            company.createDate = timezone.now()
            company.status = request.POST.get("status")
            company.author = request.user
            company.save()
            return HttpResponseRedirect("../.")
        else:
            return render(request, "company/companyEdit.html", {"company": company})
    except Company.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

def CompanyNew(request):
    try:
        if request.method == "POST":
            company = Company()
            company.name = request.POST.get("name")
            company.createDate = timezone.now()
            company.status = request.POST.get("status")
            company.author = request.user
            company.save()
            return HttpResponseRedirect("../company")
        else:
            return render(request, "company/companyCreate.html")
    except Company.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

class CompleksFilter(FilterSet):
    class Meta:
        model = Compleks
        fields = {"name": ["exact", "contains"], "status": ["exact"]}

class CompleksListView(ListView, FilterView):
    model = Compleks
    template_name = 'compleks.html'
    filterset_class = CompleksFilter

class PartnyorListView(ListView, FilterView):
    model = partnyorModel
    template_name = 'partnyor1.html'


class DutyListView(ListView, FilterView):
    model = Duty
    template_name = 'duty/duty.html'

class DutyDetail(DetailView):
    model = Duty
    template_name = "duty/duty_detail.html"

class DutyDelete(DeleteView):
    model = Duty
    template_name = 'duty/dutyDelete.html'
    success_url = reverse_lazy('duty_list')

def DutyNew(request):
    try:
        if request.method == "POST":
            duty = Duty()
            duty.duty = request.POST.get("duty")
            duty.kun = request.POST.get("kun")
            duty.oy = request.POST.get("oy")
            duty.yil = request.POST.get("yil")
            duty.createDate = timezone.now()
            duty.status = request.POST.get("status")
            duty.ticket = request.POST.get("ticket")
            duty.description = request.POST.get("description")
            duty.author = request.user
            duty.save()
            return HttpResponseRedirect("../duty")
        else:
            return render(request, "duty/dutyCreate.html")
    except Duty.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

@login_required(login_url='/accounts/login/')
def Dutyedit(request, pk):
    post = get_object_or_404(Duty, pk=pk)
    try:
        duty = Duty.objects.get(id=pk)
        if request.method == "POST":
            duty = Duty()
            duty.duty = request.POST.get("duty")
            duty.kun = request.POST.get("kun")
            duty.oy = request.POST.get("oy")
            duty.yil = request.POST.get("yil")
            duty.createDate = timezone.now()
            duty.status = request.POST.get("status")
            duty.ticket = request.POST.get("1")
            duty.description = request.POST.get("description")
            duty.author = request.user
            duty.save()
            return HttpResponseRedirect("../.")
        else:
            return render(request, "duty/dutyEdit.html", {"duty": duty})
    except Duty.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

#chart
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
    chart_data = Company.objects.annotate(month=ExtractMonth('createDate')).values('month').annotate(count=Count('id'))

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
    problems = Problem.objects.all()
    problem_names = [problem.name for problem in problems]
    ticket_counts = [Ticket.objects.filter(problem=problem).count() for problem in problems]

    context = {
        'problem_names': json.dumps(problem_names),
        'ticket_counts': json.dumps(ticket_counts),
    }
    return render(request, 'ticket_chart.html', context)

def ticket_Compleks_chart(request):
    complekss = Compleks.objects.all()
    complek_names = [complek.name for complek in complekss]
    ticket_counts = [Ticket.objects.filter(compleks=compleks).count() for compleks in complekss]

    context = {
        'compleks_names': json.dumps(complek_names),
        'ticket_counts': json.dumps(ticket_counts),
    }
    return render(request, 'ticket_chart1.html', context)
