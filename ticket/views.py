from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Problem

# def problemListView(request):
#     problems = Problem.objects.all()
#     context = {
#         "problems": problems,
#     }
#     return render(request, "home.html", context=context)
#
# def problemDetailView(request,id):
#     problem = get_object_or_404(Problem, id=id)
#     context = {
#         "problem": problem,
#     }
#     return render(request, "problem_detail.html", context=context)
class ProblemListView(ListView):
    model = Problem
    template_name = 'home.html'
    context_object_name = 'problems'

class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'problem_detail.html'