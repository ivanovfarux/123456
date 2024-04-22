"""
URL configuration for ticketProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ticket import views
from ticket.views import HomePageView, problemListView
from ticketProject.views import *

urlpatterns = [
    # path('', admin.site.urls),
    # path('ticket', include("ticket.urls")),
    # path("", homeView, name="home"),

    path('admin/', admin.site.urls),
    path('ticket', include("ticket.urls")),
    # path("", homeView, name="home"),
    path('', HomePageView.as_view(), name='home'),
    path("problems/", ProblemListView.as_view(), name="problem_list"),
    # path("partnyor/", PartnyorListView.as_view(), name="partnyor_list"),
    path("partnyor/", index(), name="index"),
    path("compleks/", CompleksListView.as_view(), name="compleks_list"),
    path("company/", CompanyListView.as_view(), name="company_list"),
    path('', include('pages.urls')),
    path('articles/', include('articles.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
