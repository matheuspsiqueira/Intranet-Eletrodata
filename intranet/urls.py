from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('etica_compliance', views.etica_compliance, name='etica_compliance',)

]