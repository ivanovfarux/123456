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
from django.http import JsonResponse
from ticket.models import Problem, Compleks, Company, Partnyor as partnyorModel, Partnyor, Ticket, Duty, Events
from django.contrib.auth.views import LoginView
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from ticket.serializer import ProblemSerializer, DutySerializer


def index(request):
    all_events = Events.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'calendar1.html', context)


def all_events(request):

    all_events = Events.objects.all()

    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })

    return JsonResponse(out, safe=False)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    return JsonResponse({})


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

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

class PartnyorListView(ListView, FilterView):
    model = Partnyor
    template_name = 'partnyor/partnyor.html'

class PartnyorDetail(DetailView):
    model = Partnyor
    template_name = "partnyor/partnyor_detail.html"

class PartnyorDelete(DeleteView):
    model = Partnyor
    template_name = 'partnyor/partnyorDelete.html'
    success_url = reverse_lazy('partnyor_list')

def PartnyorNew(request):
    companys = Company.objects.all()
    try:
        if request.method == "POST":
            partnyor = Partnyor()
            partnyor.fio = request.POST.get("fio")
            partnyor.login = request.POST.get("login")
            partnyor.password = request.POST.get("password")
            partnyor.createDate = request.POST.get("date")
            partnyor.status = timezone.now()
            partnyor.author = request.user
            partnyor.image = request.FILES.get("image")
            partnyor.contacts = request.POST.get("contacts")
            partnyor.status = request.POST.get("status")
            company_id = request.POST.get("company_id")
            partnyor.companyId = Company.objects.get(id=company_id)
            partnyor.age = request.POST.get("age")
            partnyor.save()
            return HttpResponseRedirect("../partnyor")
        else:
            return render(request, "partnyor/partnyorCreate.html", {"companys": companys})
    except Duty.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

@login_required(login_url='/accounts/login/')
def PartnyorEdit(request, pk):
        partnyors = Partnyor.objects.get(pk=pk)
        companys = Company.objects.all()
        if request.method == "POST":
            partnyors.fio = request.POST.get("fio")
            partnyors.login = request.POST.get("login")
            partnyors.password = request.POST.get("password")
            partnyors.createDate = timezone.now()
            partnyors.status = request.POST.get("status")
            partnyors.author = request.user
            partnyors.image = request.FILES.get("image")
            partnyors.contacts = request.POST.get("contacts")
            partnyors.status = request.POST.get("status")
            company_id = request.POST.get("company_id")
            partnyors.companyId = Company.objects.get(id=company_id)
            partnyors.age = request.POST.get("age")
            partnyors.save()
            return HttpResponseRedirect("../.")
        else:
            return render(request, "partnyor/partnyor_edit.html", {"partnyors": partnyors, "companys": companys})

class CompleksFilter(FilterSet):
    class Meta:
        model = Compleks
        fields = {"name": ["exact", "contains"], "status": ["exact"]}

class CompleksListView(ListView, FilterView):
    model = Compleks
    template_name = 'compleks.html'
    filterset_class = CompleksFilter

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
    tickets = Ticket.objects.all()
    try:
        if request.method == "POST":
            duty = Duty()
            duty.duty = request.user
            duty.kun = request.POST.get("kun")
            duty.oy = request.POST.get("oy")
            duty.yil = request.POST.get("yil")
            duty.createDate = timezone.now()
            duty.status = request.POST.get("status")
            ticket_id = request.POST.get("ticket_id")
            duty.ticket = Ticket.objects.get(id=ticket_id)
            duty.description = request.POST.get("description")
            duty.author = request.user
            duty.save()
            return HttpResponseRedirect("../duty")
        else:
            return render(request, "duty/dutyCreate.html", {"tickets": tickets})
    except Duty.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def Dutyedit(request, pk):
    duty = get_object_or_404(Duty, pk=pk)
    tickets = Ticket.objects.all()
    if request.method == "POST":
        duty.kun = request.POST.get("kun")
        duty.oy = request.POST.get("oy")
        duty.yil = request.POST.get("yil")
        duty.createDate = timezone.now()
        duty.status = request.POST.get("status")
        ticket_id = request.POST.get("ticket_id")
        duty.ticket = Ticket.objects.get(id=ticket_id)
        duty.description = request.POST.get("description")
        duty.author = request.user
        duty.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "duty/dutyEdit.html", {"duty": duty, "tickets": tickets})

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

def chart_data(request):
    events = Events.objects.all()
    labels = [event.name for event in events]
    data = [(event.end - event.start).total_seconds() / 3600 for event in events if event.start and event.end]  # Duration in hours

    return JsonResponse({
        'labels': labels,
        'data': data,
    })

def chart_view(request):
    return render(request, 'chart1.html')