from ticketProject import views
from ticketProject.views import ProblemListView
from django.conf import settings
from django.conf.urls.static import static
from .views import problemListView, ProblemDetailView, problem_detail, HomePageView
from django.urls import path, include

urlpatterns = [
    path("all/", problemListView, name="all_problem_list"),
    path("<int:id>/", problem_detail, name="problem_detail_page"),
    path('', include('pages.urls')),
    path('articles/', include('articles.urls')),
    # path("problems/<int:pk>/",  ProblemDetailView.as_view(), name="problem_detail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
