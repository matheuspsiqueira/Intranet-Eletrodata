from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('etica_compliance', views.etica_compliance, name='etica_compliance',)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)