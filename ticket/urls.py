from .views import ProblemListView, ProblemDetailView
from django.urls import path

urlpatterns = [
    path("",  ProblemListView.as_view(), name="problem_list_view"),
    path("problems/<int:pk>/",  ProblemDetailView.as_view(), name="problem_detail"),
]