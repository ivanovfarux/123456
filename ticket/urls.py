from django.urls import path, include
from ticket.views import *

from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()

router.register(r"problemlist", ProblemViewSet, basename="problem")
router.register(r"dutylist", DutyViewSet, basename="duty")

urlpatterns = router.urls

urlpatterns = [

    path('admin/login/', CustomLoginView.as_view(), name='login'),

    path("problems/", ProblemListView.as_view(), name="problem_list"),
    path('problems/view/<int:pk>', ProblemDetail.as_view(), name='problem_view'),
    path('problem/delete/<int:pk>', ProblemDelete.as_view(), name='problem_delete'),
    path("problems/edit/<int:pk>", edit, name='problem_edit'),
    path("problems/create", ProblemNew, name='problem_create'),

    path("company/", CompanyListView.as_view(), name="company_list"),
    path('company/view/<int:pk>', CompanyDetail.as_view(), name='company_view'),
    path('company/delete/<int:pk>', CompanyDelete.as_view(), name='company_delete'),
    path("company/edit/<int:pk>", Companyedit, name='company_edit'),
    path("company/create", CompanyNew, name='company_create'),

    path("duty/", DutyListView.as_view(), name="duty_list"),
    path('duty/view/<int:pk>', DutyDetail.as_view(), name='duty_view'),
    path('duty/delete/<int:pk>', DutyDelete.as_view(), name='duty_delete'),
    path("duty/edit/<int:pk>", Dutyedit, name='duty_edit'),
    path("duty/create", DutyNew, name='duty_create'),

    path("partnyor/", PartnyorListView.as_view(), name="partnyor_list"),
    path('partnyor/view/<int:pk>', PartnyorDetail.as_view(), name='partnyor_view'),
    path('partnyor/delete/<int:pk>', PartnyorDelete.as_view(), name='partnyor_delete'),
    path("partnyor/edit/<int:pk>", PartnyorEdit, name='partnyor_edit'),
    path("partnyor/create", PartnyorNew, name='partnyor_create'),

    path("compleks/", CompleksListView.as_view(), name="compleks_list"),
    path('compleks/view/<int:pk>', CompleksDetail.as_view(), name='compleks_view'),
    path('compleks/delete/<int:pk>/', CompleksDelete.as_view(), name='compleks_delete'),
    path("compleks/edit/<int:pk>", Compleksedit, name='compleks_edit'),
    path("compleks/create", Compleks_New, name='compleks_create'),

    path("ticket/", TicketListView.as_view(), name="ticket_list"),
    path('ticket/view/<int:pk>', TicketDetail.as_view(), name='ticket_view'),
    path('ticket/delete/<int:pk>', TicketDelete.as_view(), name='ticket_delete'),
    path("ticket/edit/<int:pk>", TicketEdit, name='ticket_edit'),
    path("ticket/create", TicketNew, name='ticket_create'),

    path("todo/", TodoListView.as_view(), name="todo_list"),
    path('todo/view/<int:pk>', TodoDetail.as_view(), name='todo_view'),
    path('todo/delete/<int:pk>', TodoDelete.as_view(), name='todo_delete'),
    path("todo/edit/<int:pk>", ToDoEdit, name='todo_edit'),
    path("todo/create", ToDoNew, name='todo_create'),

    path("education/", EducationListView.as_view(), name="education_list"),
    path('education/view/<int:pk>', EducationDetail.as_view(), name='education_view'),
    path('education/delete/<int:pk>', EducationDelete.as_view(), name='education_delete'),
    path("education/edit/<int:pk>", EducationEdit, name='education_edit'),
    path("education/create", EducationNew, name='education_create'),

    path('book/',  book_list, name='book_list'),
    path('book/create/',  book_create, name='book_create'),
    path('book/<int:pk>/update/',  book_update, name='book_update'),
    path('book/<int:pk>/delete/',  book_delete, name='book_delete'),

    path("partnyor1/", pie_chart, name="pie-chart"),

    path('chart/', chart_view, name='chart_view'),
    path('ticket_chart/', ticket_chart, name='problem_chart'),
    path('ticket_chart1/', ticket_Compleks_chart, name='compleks_chart'),

    path('calendar1/', index, name='index'),
    path('all_events/', all_events),
    path('all_duties/', all_duties),
    path('all_tickets/', all_tickets),
    path('add_event/', add_event, name='add_event'),
    path('add_duty/', add_duty, name='add_duty'),
    path('update/', update, name='update'),
    path('update_duty/', update_duty, name='update_duty'),
    path('remove/', remove, name='remove'),
    path('remove_duty', remove_duty, name='remove_duty'),
    path('chart1/', chart_data, name='chart_data'),
    path('chart2/', chart_view, name='chart_view'),
]
