from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django_filters.views import FilterView
from django_filters import FilterSet
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, UserProfileForm, UserEditForm
from django.http import JsonResponse
from ticket.models import Problem, Compleks, Company, Partnyor, Ticket, Duty, Events, \
    Education, ToDo, ReadEducationLog
from django.contrib.auth.views import LoginView, LogoutView
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import LoginHistory
from .forms import TicketForm, EventsForm, ToDoForm

@login_required
def index(request):
    duties = Duty.objects.all()
    users = User.objects.all()
    tickets = Ticket.objects.all()
    events = Events.objects.all()

    if request.user.is_authenticated:
        # If user is authenticated, fetch todos associated with the user
        todos = ToDo.objects.filter(user=request.user)
    else:
        # If user is not authenticated, set todos to an empty list
        todos = []
    context = {
        "duties": duties,
        "users": users,
        "tickets": tickets,
        "todos": todos,
        "events": events,
    }
    return render(request, 'calendar1.html', context)

def all_events(request):
    duties = Duty.objects.all()
    events = Events.objects.all()
    if request.user.is_authenticated:
        # If user is authenticated, fetch todos associated with the user
        todos = ToDo.objects.filter(user=request.user)
        todos = ToDo.objects.filter(status=True)
        tickets = Ticket.objects.filter(user=request.user, status=True)
        tickets = Ticket.objects.filter(status=True)
    else:
        todos = []
        tickets = []

    out = []
    for duty in duties:
        out.append({
            'id': duty.id,
            'title': duty.duty.first_name + ' ' + duty.duty.username + ' ' + duty.duty.last_name,
            'start': duty.start.strftime("%Y-%m-%d"),
            'end': duty.end.strftime("%Y-%m-%d"),
            'color': duty.color if duty.color else '#198754',
            'model': 'duty'
        })
    for ticket in tickets:
        out.append({
            'id': ticket.id,
            'title': ticket.name,
            'start': ticket.start.strftime("%Y-%m-%d"),
            'end': ticket.end.strftime("%Y-%m-%d"),
            'color': ticket.color if ticket.color else '#0d6efd',
            'model': 'ticket'
        })
    for todo in todos:
        out.append({
            'id': todo.id,
            'title': todo.name,
            'start': todo.start.strftime("%Y-%m-%d"),
            'end': todo.end.strftime("%Y-%m-%d"),
            'color': todo.color if todo.color else '#ffc107',
            'model': 'todo'
        })
    for event in events:
        if request.user == event.author:
            out.append({
                'id': event.id,
                'title': event.name,
                'start': event.start.strftime("%Y-%m-%d"),
                'end': event.end.strftime("%Y-%m-%d"),
                'color': event.color if event.color else '#ffc107',
                'model': 'event'
            })
    return JsonResponse(out, safe=False)

def events(request):
    events = Events.objects.all()
    out = []
    for event in events:
        out.append({
            'id': event.id,
            'title': event.name,
            'start': event.start.strftime("%Y-%m-%d"),
            'end': event.end.strftime("%Y-%m-%d"),
            'color': event.color if event.color else '#198754',
            'event': True
        })
    return JsonResponse(out, safe=False)

def all_duties(request):
    duties = Duty.objects.all()
    out = []
    for duty in duties:
        out.append({
            'id': duty.id,
            'title': duty.duty.username,
            'start': duty.start.strftime("%Y-%m-%d"),
            'end': duty.end.strftime("%Y-%m-%d"),
            'color': duty.color if duty.color else '#198754',
            'duty': True
        })
    return JsonResponse(out, safe=False)

def all_tickets(request):
    tickets = Ticket.objects.filter(status='true')
    out = []
    for ticket in tickets:
        out.append({
            'id': ticket.id,
            'title': ticket.name,
            'start': ticket.start.strftime("%Y-%m-%d"),
            'end': ticket.end.strftime("%Y-%m-%d"),
            'color': ticket.color if ticket.color else '#0d6efd',
            'ticket': True
        })

    return JsonResponse(out, safe=False)

def add_duty(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    user_id = int(request.GET.get("user_id", 0))
    user = User.objects.get(pk=user_id)
    duty = Duty(duty=user, author=user, start=start, end=end)
    duty.save()
    return JsonResponse({})

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    name = request.GET.get("name", None)
    color = request.GET.get("color", None)
    event = Events(name=str(name), color=color, start=start, end=end)
    event.save()
    return JsonResponse({})

def update(request):
    id = request.GET.get("id", None)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    model_name = request.GET.get("model", None)
    model = Events
    if model_name == 'duty':
        model = Duty
    elif model_name == 'ticket':
        model = Ticket
    elif model_name == 'todo':
        model = ToDo
    event = get_object_or_404(model, pk=id)
    event.start = start
    event.end = end
    event.save()
    return JsonResponse({})

def update_duty(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    id = request.GET.get("id", None)
    duty = Duty.objects.get(id=id)
    duty.start = start
    duty.end = end
    duty.save()
    data = {}
    return JsonResponse(data)

def remove(request):
    id = request.GET.get("id", None)
    ticket = request.GET.get("ticket", None)
    duty = request.GET.get("duty", None)
    todo = request.GET.get("todo", None)
    if ticket:
        Ticket.objects.get(id=id).delete()
    if duty:
        Duty.objects.get(id=id).delete()
    if todo:
        ToDo.objects.get(id=id).delete()

    return JsonResponse({})

def remove_duty(request):
    id = request.GET.get("id", None)
    duty = Duty.objects.get(id=id)
    duty.delete()
    return JsonResponse({})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

def get_success_url(self):
    return reverse_lazy('tasks')

class CustomLogoutView(LogoutView):
    template_name = 'login.html'

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
            # problem.status = request.POST.get("status")
            if 'status' in request.POST and request.POST['status'] == 'on':
                problem.status = True
            else:
                problem.status = False
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
            # print("status 222  "+request.POST.get("status"))
            if 'status' in request.POST and request.POST['status'] == 'on':
                problem.status = True
            else:
                problem.status = False

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
            if 'status' in request.POST and request.POST['status'] == 'on':
                company.status = True
            else:
                company.status = False
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
            if 'status' in request.POST and request.POST['status'] == 'on':
                company.status = True
            else:
                company.status = False
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
            if 'status' in request.POST and request.POST['status'] == 'on':
                partnyor.status = True
            else:
                partnyor.status = False
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
        if 'status' in request.POST and request.POST['status'] == 'on':
            partnyors.status = True
        else:
            partnyors.status = False
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
        if 'status' in request.POST and request.POST['status'] == 'on':
            compleks.status = True
        else:
            compleks.status = False
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
        if 'status' in request.POST and request.POST['status'] == 'on':
            compleks.status = True
        else:
            compleks.status = False
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
            if 'status' in request.POST and request.POST['status'] == 'on':
                duty.status = True
            else:
                duty.status = False
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
        duty.description = request.POST.get("description")
        duty.author = request.user
        if 'status' in request.POST and request.POST['status'] == 'on':
            duty.status = True
        else:
            duty.status = False
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
    ticket_users = ticket.user.all()
    # selected_users = ticket.user.all()
    compleks = Compleks.objects.all()
    companys = Company.objects.all()
    problems = Problem.objects.all()
    partnyors = Partnyor.objects.all()
    if request.method == "POST":
        ticket.name = request.POST.get("name")
        ticket.note = request.POST.get("note")
        ticket.color = request.POST.get("color")
        compleks_id = request.POST.get("compleks_id")
        ticket.compleks = Compleks.objects.get(id=compleks_id)
        problem_id = request.POST.get("problem_id")
        ticket.problem = Problem.objects.get(id=problem_id)
        company_id = request.POST.get("company_id")
        ticket.company = Company.objects.get(id=company_id)
        user_id = request.POST.getlist("user_id")
        for user_id in user_id:
            user = get_object_or_404(User, id=user_id)
            ticket.user.add(user)
        # ticket.user = User.objects.get(id=user_id)
        partnyor_id = request.POST.get("partnyor_id")
        ticket.partnyor = Partnyor.objects.get(id=partnyor_id)
        ticket.name = request.POST.get("name")
        ticket.createDate = timezone.now()
        ticket.start = request.POST.get("start")
        if 'status' in request.POST and request.POST['status'] == 'on':
            ticket.status = True
        else:
            ticket.status = False
        ticket.end = request.POST.get("end")
        ticket.file = request.FILES.get("file")
        ticket.author = request.user
        ticket.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "ticket/ticket_edit.html", {"ticket": ticket, "users": users,
                                                           "ticket_users": ticket_users,
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
        ticket.color = request.POST.get("color")
        compleks_id = request.POST.get("compleks_id")
        ticket.compleks = Compleks.objects.get(id=compleks_id)

        problem_id = request.POST.get("problem_id")
        ticket.problem = Problem.objects.get(id=problem_id)

        company_id = request.POST.get("company_id")
        ticket.company = Company.objects.get(id=company_id)
        ticket.author = request.user
        partnyor_id = request.POST.get("partnyor_id")
        ticket.partnyor = Partnyor.objects.get(id=partnyor_id)

        user_id = request.POST.getlist("user_id")
        ticket.save()
        for user_id in user_id:
            user = get_object_or_404(User, id=user_id)
            ticket.user.add(user)
        ticket.file = request.FILES.get("file")
        ticket.createDate = timezone.now()
        ticket.start = request.POST.get("start")
        ticket.end = request.POST.get("end")
        if 'status' in request.POST and request.POST['status'] == 'on':
            ticket.status = True
        else:
            ticket.status = False
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

@login_required
def mark_education_as_read(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    # Mark the education as read
    education.mark_as_read(request.user)

    # Log the action in the database
    ReadEducationLog.objects.create(user=request.user, education=education)

    return redirect('education_view', pk=education_id)

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
            if 'status' in request.POST and request.POST['status'] == 'on':
                education.status = True
            else:
                education.status = False
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
        if 'status' in request.POST and request.POST['status'] == 'on':
            educations.status = True
        else:
            educations.status = False
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
def ToDoNew(request, mode: str = None):
    users = User.objects.all()
    complekss = Compleks.objects.all()

    try:
        if request.method == "POST":
            todo = ToDo()
            todo.name = request.POST.get("name")
            todo.note = request.POST.get("note")
            compleks_id = request.POST.get("compleks_id")
            todo.author = request.user
            todo.updatedDate = timezone.now()
            todo.start = request.POST.get("start")
            todo.end = request.POST.get("end")
            todo.color = request.POST.get("color")
            todo.compleks = Compleks.objects.get(id=compleks_id)
            user_id = request.POST.getlist("user_id")
            todo.save()
            for user_id in user_id:
                user = get_object_or_404(User, id=user_id)
                todo.user.add(user)

            if 'status' in request.POST and request.POST['status'] == 'on':
                todo.status = True
            else:
                todo.status = False
            todo.file = request.FILES.get("file", None)
            todo.save()
            return HttpResponseRedirect("../todo")
        else:
            return render(request, "todo/todoCreate.html", {"users": users, "complekss": complekss})
    except ToDo.DoesNotExist:
        return HttpResponseNotFound("<h2>todo not found</h2>")

def todoAjax(request):
    users = User.objects.all()
    complekss = Compleks.objects.all()
    return render("todo/todoCreate.html", {"users": users, "complekss": complekss}, def_name='modal')

@login_required(login_url='/accounts/login/')
def ToDoEdit(request, pk):
    todo = ToDo.objects.get(pk=pk)
    users = User.objects.all()
    complekss = Compleks.objects.all()
    companys = Company.objects.all()
    todo_users=todo.user.all()
    if request.method == "POST":
        todo.name = request.POST.get("name")
        todo.note = request.POST.get("note")
        compleks_id = request.POST.get("compleks_id")
        todo.compleks = Compleks.objects.get(id=compleks_id)
        user_id = request.POST.getlist("user_id")
        todo.user.clear()
        for user_id in user_id:
            user = get_object_or_404(User, id=user_id)
            todo.user.add(user)
        todo.updatedDate = timezone.now()
        todo.author = request.user
        todo.start = request.POST.get("start")
        todo.end = request.POST.get("end")
        todo.color = request.POST.get("color")
        if 'status' in request.POST and request.POST['status'] == 'on':
            todo.status = True
        else:
            todo.status = False
        todo.file = request.FILES.get("file", None)
        todo.save()
        return HttpResponseRedirect("../.")
    else:
        return render(request, "todo/todo_edit.html", {"users": users, "complekss": complekss, "todo_users": todo_users, "todo": todo})

class EventFilter(FilterSet):
    class Meta:
        model = Compleks
        fields = {"name": ["exact", "contains"], "status": ["exact"]}

class EventListView(ListView, FilterView):
    model = Events
    template_name = 'event/event.html'
    context_object_name = 'events'

class EventDetail(DetailView):
    model = Events
    template_name = "event/event_detail.html"

class EventDelete(DeleteView):
    model = Events
    template_name = 'event/eventDelete.html'
    success_url = reverse_lazy('event_list')

@login_required(login_url='/accounts/login/')
def EventEdit(request, pk):
    post = get_object_or_404(Events, pk=pk)
    try:
        event = Events.objects.get(id=pk)
        if request.method == "POST":
            event.name = request.POST.get("name")
            event.start = request.POST.get("start")
            event.end = request.POST.get("end")
            event.color = request.POST.get("color")
            event.author = request.user
            event.createDate = timezone.now()
            # print("status 222  "+request.POST.get("status"))
            if 'status' in request.POST and request.POST['status'] == 'on':
                event.status = True
            else:
                event.status = False
            event.save()
            return HttpResponseRedirect("../.")
        else:
            return render(request, "event/eventEdit.html", {"event": event})
    except Events.DoesNotExist:
        return HttpResponseNotFound("<h2>Event not found</h2>")

def EventNew(request):
    try:
        if request.method == "POST":
            event = Events()
            event.name = request.POST.get("name")
            event.start = request.POST.get("start")
            event.end = request.POST.get("end")
            event.color = request.POST.get("color")
            if 'status' in request.POST and request.POST['status'] == 'on':
                event.status = True
            else:
                event.status = False
            event.author = request.user
            event.createDate = timezone.now()

            event.save()
            return HttpResponseRedirect("../event")
        else:
            return render(request, "event/eventCreate.html")
    except Events.DoesNotExist:
        return HttpResponseNotFound("<h2>Event not found</h2>")

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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
        profile_form = UserProfileForm()
    return render(request, 'signup.html', {'form': form, 'profile_form': profile_form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def user_login_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    login_history = LoginHistory.objects.filter(user=user).order_by('-login_time')
    # Process login history as needed
    return render(request, 'login_history.html', {'login_history': login_history})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = TicketForm()
    return render(request, 'calendar1.html', {'form': form})


def ticket_form_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect after successful form submission
    else:
        form = TicketForm()

    return render(request, 'ticket_form.html', {'ticket_form': form})

def create_event(request):
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = EventsForm()
    return render(request, 'event_form.html', {'form': form})

def create_todo(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = ToDoForm()
    return render(request, 'todo_form.html', {'form': form})