from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ticket.urls import router
from ticketProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ticket.urls')),
    path('api/', include(router.urls))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
