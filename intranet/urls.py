from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('etica_compliance', views.etica_compliance, name='etica_compliance'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('api/status_servicos', views.status_servicos, name='status_servicos'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)