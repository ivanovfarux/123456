from ticketProject import views
# from ticketProject.views import ProblemListView
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.urls import path, include

urlpatterns = [
    # path("all/", problemListView, name="all_problem_list"),
    # path('', include('pages.urls')),
    # path('articles/', include('articles.urls')),
    # path("", homeView, name="home"),
    # path('', HomePageView.as_view(), name='home'),


    path("problems/", ProblemListView.as_view(), name="problem_list"),
    path('problems/view/<int:pk>',  ProblemDetail.as_view(), name='problem_view'),
    path('problems/edit/<int:pk>', ProblemUpdateView.as_view(), name='problem_edit'),
    path('problems/create', ProblemCreateView.as_view(), name='problem_create'),
    path('problem/delete/<int:pk>', ProblemDelete.as_view(), name='problem_delete'),
    path("partnyor1/", PartnyorListView.as_view(), name="partnyor_list"),
    path("partnyor/", Partnyor, name="chart_view"),
    path("compleks/", CompleksListView.as_view(), name="compleks_list"),
    path("company/", CompanyListView.as_view(), name="company_list"),
]