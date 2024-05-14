from .views import *
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/login/', CustomLoginView.as_view(), name='login'),
    path("problems/", ProblemListView.as_view(), name="problem_list"),
    path('problems/view/<int:pk>',  ProblemDetail.as_view(), name='problem_view'),
    # path('problems/edit/<int:pk>', problem_update, name='problem_edit'),
    # path('problems/create', ProblemCreateView.as_view(), name='problem_create'),
    # path('problems/edit/<int:pk>', TodoUpdateView.as_view(), name='problem_edit'),
    path("problems/edit/<int:pk>", edit, name='problem_edit'),
    path("problems/create", ProblemNew, name='problem_create'),
    # path('create/', YourCreateView.as_view(), name='create_view_name'),
    path('problem/delete/<int:pk>', ProblemDelete.as_view(), name='problem_delete'),
    path("partnyor1/", PartnyorListView.as_view(), name="partnyor_list"),
    path("partnyor/", pie_chart, name="pie-chart"),
    path("compleks/", CompleksListView.as_view(), name="compleks_list"),
    path("company/", CompanyListView.as_view(), name="company_list"),
    path('chart/',  chart_view, name='chart_view'),
    path('ticket_chart/', ticket_chart, name='ticket_chart'),

]
