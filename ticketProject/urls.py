from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from ticket.views import HomePageView
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
    path("partnyor1/", PartnyorListView.as_view(), name="partnyor_list"),
    path("partnyor/", views.chart_view, name="chart_view"),
    path("compleks/", CompleksListView.as_view(), name="compleks_list"),
    path("company/", CompanyListView.as_view(), name="company_list"),
    path('', include('pages.urls')),
    path('articles/', include('articles.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
