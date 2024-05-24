from django.urls import path, include
from ticket.views import *

from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()

router.register(r"problemlist", ProblemViewSet, basename="problem")
router.register(r"dutylist", DutyViewSet, basename="duty")

urlpatterns = router.urls

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/login/', CustomLoginView.as_view(), name='login'),
    path("problems/", ProblemListView.as_view(), name="problem_list"),
    path('problems/view/<int:pk>',  ProblemDetail.as_view(), name='problem_view'),
    path("problems/edit/<int:pk>", edit, name='problem_edit'),
    path("problems/create", ProblemNew, name='problem_create'),
    path('problem/delete/<int:pk>', ProblemDelete.as_view(), name='problem_delete'),
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

    # path('problems/edit/<int:pk>', problem_update, name='problem_edit'),
    # path('problems/create', ProblemCreateView.as_view(), name='problem_create'),
    # path('problems/edit/<int:pk>', TodoUpdateView.as_view(), name='problem_edit'),
    path("partnyor1/", PartnyorListView.as_view(), name="partnyor_list"),
    path("partnyor/", pie_chart, name="pie-chart"),
    path("compleks/", CompleksListView.as_view(), name="compleks_list"),
    path('chart/',  chart_view, name='chart_view'),
    path('ticket_chart/', ticket_chart, name='problem_chart'),
    path('ticket_chart1/', ticket_Compleks_chart, name='compleks_chart'),

    path('calendar1/',  index, name='index'),
    path('all_events/',  all_events, name='all_events'),
    path('add_event/',  add_event, name='add_event'),
    path('update/',  update, name='update'),
    path('remove/',  remove, name='remove'),
]
