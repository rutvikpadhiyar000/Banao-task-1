from django.urls import path

from . import views

urlpatterns = [
    path("getjobnames/", views.getjobnames, name="getjobnames"),
    path("getjob/<str:jobname>", views.getjobs, name="getjobs"),
]
