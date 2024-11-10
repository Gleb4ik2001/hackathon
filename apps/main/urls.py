from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import MainView

urlpatterns = [
    path('main/', MainView.as_view(), name='main_view'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )