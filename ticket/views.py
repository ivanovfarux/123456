from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django_filters.views import FilterView
from django_filters import FilterSet
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from ticket.models import Problem, Compleks, Company, Partnyor, Ticket, Duty, Events, \
    Education, ToDo
from django.contrib.auth.views import LoginView
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from ticket.serializer import ProblemSerializer, DutySerializer


def index(request):
    duties = Duty.objects.all()
    users = User.objects.all()
    context = {
        "duties": duties,
        "users": users,
    }
    return render(request, 'calendar1.html', context)

def all_events(request):
    all_events = Events.objects.all()

    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%Y-%m-%d"),
            'end': event.end.strftime("%Y-%m-%d"),
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

class DutyViewSet(viewsets.ViewSet):
    def list(self, request):
        duty = Duty.objects.all()
        serializer = DutySerializer(duty, many=True)
        return Response(serializer.data)

class ProblemViewSet(viewsets.ViewSet):
    def list(self, request):
        stu = Problem.objects.all()
        serializer = ProblemSerializer(stu, many=True)
        return Response(serializer.data)

class ProblemListView(ListView, FilterView):
    model = Problem
    template_name = 'problems/problem.html'

class ProblemDetail(DetailView):
    model = Problem
    template_name = "problems/problem_detail.html"

class ProblemDelete(DeleteView):
    model = Problem
    template_name = 'problems/problemDelete.html'
    success_url = reverse_lazy('problem_list')

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

@login_required(login_url='/accounts/login/')
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
    template_name = 'compleks/compleks.html'
    filterset_class = CompleksFilter

class CompleksDetail(DetailView):
    model = Compleks
    template_name = "compleks/compleks_detail.html"

class CompleksDelete(DeleteView):
    model = Compleks
    template_name = 'compleks/compleksDelete.html'
    success_url = reverse_lazy('compleks_list')

def Compleksedit(request, pk):
    compleks = get_object_or_404(Compleks, pk=pk)
    if request.method == "POST":
        compleks.name = request.POST.get("name")
        compleks.documents = request.FILES.get("documents")
        compleks.schema_net = request.FILES.get("schema_net")
        compleks.createDate = timezone.now()
        compleks.status = request.POST.get("status")
        compleks.author = request.user
        compleks.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "compleks/compleks_edit.html", {"compleks": compleks})

def Compleks_New(request):
    if request.method == "POST":
        compleks = Compleks()
        compleks.name = request.POST.get("name")
        compleks.documents = request.FILES.get("documents")
        compleks.schema_net = request.FILES.get("schema_net")
        compleks.createDate = timezone.now()
        compleks.status = request.POST.get("status")
        compleks.author = request.user
        compleks.save()
        return HttpResponseRedirect("../compleks")
    else:
        return render(request, "compleks/compleksCreate.html")

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
    users = User.objects.all()
    try:
        if request.method == "POST":
            duty = Duty()
            duty.createDate = timezone.now()
            duty.status = request.POST.get("status")
            duty.description = request.POST.get("description")
            duty.author = request.user
            user_id = request.POST.get("user_id")
            duty.duty = User.objects.get(id=user_id)
            duty.start = request.POST.get("start")
            duty.end = request.POST.get("end")
            duty.color = request.POST.get("color")
            duty.save()
            return HttpResponseRedirect("../duty")
        else:
            return render(request, "duty/dutyCreate.html", {"users": users})
    except Duty.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

def Dutyedit(request, pk):
    duty = get_object_or_404(Duty, pk=pk)
    users = User.objects.all()
    if request.method == "POST":
        duty.status = request.POST.get("status")
        duty.description = request.POST.get("description")
        duty.author = request.user
        user_id = request.POST.get("user_id")
        duty.duty = User.objects.get(id=user_id)
        duty.createDate = timezone.now()
        duty.start = request.POST.get("start")
        duty.end = request.POST.get("end")
        duty.color = request.POST.get("color")

        duty.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "duty/dutyEdit.html", {"duty": duty, "users": users})

class TicketListView(ListView, FilterView):
    model = Ticket
    template_name = 'ticket/ticket.html'

class TicketDetail(DetailView):
    model = Ticket
    template_name = "ticket/ticket_detail.html"

class TicketDelete(DeleteView):
    model = Ticket
    template_name = 'ticket/ticketDelete.html'
    success_url = reverse_lazy('ticket_list')

@login_required(login_url='/accounts/login/')
def TicketEdit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    users = User.objects.all()
    compleks = Compleks.objects.all()
    companys = Company.objects.all()
    problems = Problem.objects.all()
    partnyors = Partnyor.objects.all()
    if request.method == "POST":
        ticket.name = request.POST.get("name")
        ticket.note = request.POST.get("note")
        compleks_id = request.POST.get("compleks_id")
        ticket.compleks = Compleks.objects.get(id=compleks_id)
        problem_id = request.POST.get("problem_id")
        ticket.problem = Problem.objects.get(id=problem_id)
        company_id = request.POST.get("company_id")
        ticket.company = Company.objects.get(id=company_id)
        user_id = request.POST.get("user_id")
        ticket.user = User.objects.get(id=user_id)
        partnyor_id = request.POST.get("partnyor_id")
        ticket.partnyor = Partnyor.objects.get(id=partnyor_id)
        ticket.name = request.POST.get("name")
        ticket.createDate = timezone.now()
        ticket.start = request.POST.get("start")
        ticket.end = request.POST.get("end")
        ticket.file = request.FILES.get("file")
        ticket.status = request.POST.get("status")
        ticket.author = request.user
        ticket.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "ticket/ticket_edit.html", {"ticket": ticket, "users": users,
                                                           "compleks": compleks, "partnyors": partnyors,
                                                           "companys": companys, "problems": problems})

def TicketNew(request):
    users = User.objects.all()
    complekss = Compleks.objects.all()
    companys = Company.objects.all()
    problems = Problem.objects.all()
    partnyors = Partnyor.objects.all()

    if request.method == "POST":
        ticket = Ticket()
        ticket.name = request.POST.get("name")
        ticket.note = request.POST.get("note")

        compleks_id = request.POST.get("compleks_id")
        ticket.compleks = Compleks.objects.get(id=compleks_id)

        problem_id = request.POST.get("problem_id")
        ticket.problem = Problem.objects.get(id=problem_id)

        company_id = request.POST.get("company_id")
        ticket.company = Company.objects.get(id=company_id)

        user_id = request.POST.get("user_id")
        ticket.user = User.objects.get(id=user_id)

        partnyor_id = request.POST.get("partnyor_id")
        ticket.partnyor = Partnyor.objects.get(id=partnyor_id)
        ticket.file = request.FILES.get("file")
        ticket.name = request.POST.get("name")
        ticket.createDate = timezone.now()
        ticket.start = request.POST.get("start")
        ticket.end = request.POST.get("end")
        ticket.status = request.POST.get("status")
        ticket.author = request.user
        ticket.save()
        return HttpResponseRedirect("../ticket")
    else:
        return render(request, "ticket/ticketCreate.html", {"users": users, "complekss": complekss,
                                                            "companys": companys, "problems": problems,
                                                            "partnyors": partnyors})


class EducationListView(ListView, FilterView):
    model = Education
    template_name = 'education/education.html'

class EducationDetail(DetailView):
    model = Education
    template_name = "education/education_detail.html"

class EducationDelete(DeleteView):
    model = Education
    template_name = 'education/educationDelete.html'
    success_url = reverse_lazy('education_list')

@login_required(login_url='/accounts/login/')
def EducationNew(request):
    users = User.objects.all()
    try:
        if request.method == "POST":
            education = Education()
            education.name = request.POST.get("name")
            education.info = request.POST.get("info")
            education.date = request.POST.get("date")
            education.createDate = timezone.now()
            education.status = request.POST.get("status")
            education.author = request.user
            education.file = request.FILES.get("file")
            education.read = request.POST.get("read")
            education.toDate = request.POST.get("toDate")
            education.endDate = request.POST.get("endDate")
            user_id = request.POST.get("user_id")
            education.teacher = User.objects.get(id=user_id)
            education.save()
            return HttpResponseRedirect("../education")
        else:
            return render(request, "education/educationCreate.html", {"users": users})
    except Education.DoesNotExist:
        return HttpResponseNotFound("<h2>education not found</h2>")

@login_required(login_url='/accounts/login/')
def EducationEdit(request, pk):
    educations = Education.objects.get(pk=pk)
    users = User.objects.all()
    if request.method == "POST":
        educations.name = request.POST.get("name")
        user_id = request.POST.get("user_id")
        educations.teacher = User.objects.get(id=user_id)
        educations.info = request.POST.get("info")
        educations.date = request.POST.get("date")
        educations.createDate = timezone.now()
        educations.status = request.POST.get("status")
        educations.author = request.user
        educations.file = request.FILES.get("file")
        educations.read = request.POST.get("read")
        educations.toDate = request.POST.get("toDate")
        educations.endDate = request.POST.get("endDate")
        educations.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "education/education_edit.html", {"educations": educations, "users": users})

class TodoListView(ListView, FilterView):
    model = ToDo
    template_name = 'todo/todo.html'

class TodoDetail(DetailView):
    model = ToDo
    template_name = "todo/todo_detail.html"

class TodoDelete(DeleteView):
    model = ToDo
    template_name = 'todo/todoDelete.html'
    success_url = reverse_lazy('todo_list')

@login_required(login_url='/accounts/login/')
def ToDoNew(request):
    users = User.objects.all()
    complekss = Compleks.objects.all()

    try:
        if request.method == "POST":
            todo = ToDo()
            todo.name = request.POST.get("name")
            todo.note = request.POST.get("note")
            compleks_id = request.POST.get("compleks_id")
            todo.compleks = Compleks.objects.get(id=compleks_id)
            user_id = request.POST.get("user_id")
            todo.user = User.objects.get(id=user_id)
            todo.updatedDate = timezone.now()
            todo.author = request.user
            todo.start = request.GET.get("start")
            todo.end = request.GET.get("end")
            todo.color = request.POST.get("color")
            todo.status = request.POST.get("status")
            todo.file = request.FILES.get("file", None)
            todo.save()
            return HttpResponseRedirect("../todo")
        else:
            return render(request, "todo/todoCreate.html", {"users": users, "complekss": complekss})
    except ToDo.DoesNotExist:
        return HttpResponseNotFound("<h2>todo not found</h2>")


@login_required(login_url='/accounts/login/')
def ToDoEdit(request, pk):
    todo = ToDo.objects.get(pk=pk)
    users = User.objects.all()
    complekss = Compleks.objects.all()
    companys = Company.objects.all()

    if request.method == "POST":
        todo.name = request.POST.get("name")
        todo.note = request.POST.get("note")
        compleks_id = request.POST.get("compleks_id")
        todo.compleks = Compleks.objects.get(id=compleks_id)
        user_id = request.POST.get("user_id")
        todo.user = User.objects.get(id=user_id)
        todo.updatedDate = timezone.now()
        todo.author = request.user
        todo.start = request.GET.get("start")
        todo.end = request.GET.get("end")
        todo.color = request.POST.get("color")
        todo.status = request.POST.get("status")
        todo.file = request.FILES.get("file", None)
        todo.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "todo/todo_edit.html", { "users": users, "complekss": complekss, "todo": todo})


# chart
def chart_view(request):
    partnyor_data = Partnyor.objects.all()
    return render(request, 'partnyor.html', {'partnyor_data': partnyor_data})

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
    data = [(event.end - event.start).total_seconds() / 3600 for event in events if
            event.start and event.end]  # Duration in hours
    return JsonResponse({
        'labels': labels,
        'data': data,
    })


def chart_view(request):
    return render(request, 'chart1.html')
# 