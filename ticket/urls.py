from django.urls import path


from ticket.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = router.urls

urlpatterns = [

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('login-history/<int:user_id>/', user_login_history, name='user_login_history'),
    path("problems/", login_required(ProblemListView.as_view()), name="problem_list"),
    path('problems/view/<int:pk>', login_required(ProblemDetail.as_view()), name='problem_view'),
    path('problem/delete/<int:pk>', login_required(ProblemDelete.as_view()), name='problem_delete'),
    path("problems/edit/<int:pk>", login_required(edit), name='problem_edit'),
    path("problems/create", login_required(ProblemNew), name='problem_create'),

    path("company/", login_required(CompanyListView.as_view()), name="company_list"),
    path('company/view/<int:pk>', login_required(CompanyDetail.as_view()), name='company_view'),
    path('company/delete/<int:pk>', login_required(CompanyDelete.as_view()), name='company_delete'),
    path("company/edit/<int:pk>", login_required(Companyedit), name='company_edit'),
    path("company/create", login_required(CompanyNew), name='company_create'),

    path("compleks/", login_required(CompleksListView.as_view()), name="compleks_list"),
    path('compleks/view/<int:pk>', login_required(CompleksDetail.as_view()), name='compleks_view'),
    path('compleks/delete/<int:pk>/', login_required(CompleksDelete.as_view()), name='compleks_delete'),
    path("compleks/edit/<int:pk>", login_required(Compleksedit), name='compleks_edit'),
    path("compleks/create", login_required(Compleks_New), name='compleks_create'),

    path("partnyor/", login_required(PartnyorListView.as_view()), name="partnyor_list"),
    path('partnyor/view/<int:pk>', login_required(PartnyorDetail.as_view()), name='partnyor_view'),
    path('partnyor/delete/<int:pk>', login_required(PartnyorDelete.as_view()), name='partnyor_delete'),
    path("partnyor/edit/<int:pk>", login_required(PartnyorEdit), name='partnyor_edit'),
    path("partnyor/create", login_required(PartnyorNew), name='partnyor_create'),

    path("education/", login_required(EducationListView.as_view()), name="education_list"),
    path('education/view/<int:pk>', login_required(EducationDetail.as_view()), name='education_view'),
    path('education/delete/<int:pk>', login_required(EducationDelete.as_view()), name='education_delete'),
    path("education/edit/<int:pk>", login_required(EducationEdit), name='education_edit'),
    path("education/create", login_required(EducationNew), name='education_create'),
    path('education/<int:education_id>/mark-read/', mark_education_as_read, name='mark_education_as_read'),
    # path('education/<int:pk>/', EducationDetailView.as_view(), name='education_detail'),
    path("ticket/", login_required(TicketListView.as_view()), name="ticket_list"),
    path('ticket/view/<int:pk>', login_required(TicketDetail.as_view()), name='ticket_view'),
    path('ticket/delete/<int:pk>', login_required(TicketDelete.as_view()), name='ticket_delete'),
    path("ticket/edit/<int:pk>", login_required(TicketEdit), name='ticket_edit'),
    path("ticket/create", login_required(TicketNew), name='ticket_create'),

    path("todo/", login_required(TodoListView.as_view()), name="todo_list"),
    path('todo/view/<int:pk>', login_required(TodoDetail.as_view()), name='todo_view'),
    path('todo/delete/<int:pk>', login_required(TodoDelete.as_view()), name='todo_delete'),
    path("todo/edit/<int:pk>", login_required(ToDoEdit), name='todo_edit'),
    path("todo/create", login_required(ToDoNew), name='todo_create'),

    path("duty/", login_required(DutyListView.as_view()), name="duty_list"),
    path('duty/view/<int:pk>', login_required(DutyDetail.as_view()), name='duty_view'),
    path('duty/delete/<int:pk>', login_required(DutyDelete.as_view()), name='duty_delete'),
    path("duty/edit/<int:pk>", login_required(Dutyedit), name='duty_edit'),
    path("duty/create", login_required(DutyNew), name='duty_create'),

    path("event/", login_required(EventListView.as_view()), name="event-list"),
    path('event/view/<int:pk>', login_required(EventDetail.as_view()), name='event_view'),
    path('event/delete/<int:pk>', login_required(EventDelete.as_view()), name='event_delete'),
    path("event/edit/<int:pk>", login_required(EventEdit), name='event_edit'),
    path("event/create", login_required(EventNew), name='event_create'),

    path('create-ticket/', create_ticket, name='create_ticket'),
    path('create-event/', create_event, name='create_event'),
    path('create-todo/', create_todo, name='create_todo'),

    path("partnyor1/", login_required(pie_chart), name="pie-chart"),
    path('chart/', login_required(chart_view), name='chart_view'),
    path('ticket_chart/', login_required(ticket_chart), name='problem_chart'),
    path('ticket_chart1/', login_required(ticket_Compleks_chart), name='compleks_chart'),

    path('', login_required(index), name='base'),
    path('calendar1/', login_required(index), name='index'),
    path('all_events/', login_required(all_events)),
    path('all_duties/', login_required(all_duties)),
    path('all_tickets/', login_required(all_tickets)),
    path('add_event/', login_required(add_event), name='add_event'),
    path('add_duty/', login_required(add_duty), name='add_duty'),
    path('update/', login_required(update), name='update'),
    path('update_duty/', login_required(update_duty), name='update_duty'),
    path('remove/', login_required(remove), name='remove'),
    path('remove_duty', login_required(remove_duty), name='remove_duty'),
    path('chart1/', login_required(chart_data), name='chart_data'),
    path('chart2/', login_required(chart_view), name='chart_view'),
]
