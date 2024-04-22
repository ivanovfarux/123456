from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from .models import Problem, Partnyor


def problemListView(request):
    # problems_list = Problem.objects.all()
    problems_list = Problem.Activ.all()
    # problems_list = Problem.objects.filter(status=Problem.Status.Activ)
    context = {
        "problems_list": problems_list,
    }
    return render(request, "home.html", context=context)



class HomePageView(TemplateView):
    model = Problem
    template_name = 'home.html'

def problem_detail(request, id):
    problems = get_object_or_404(Problem, id=id, status=Problem.Status.Activ)
    context = {
        "problems": problems,
    }
    return render(request, "tickets/problem_detail.html", context=context)



class ProblemListView(ListView):
    model = Problem
    template_name = 'home.html'
    context_object_name = 'problems'


class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'problem_detail.html'


