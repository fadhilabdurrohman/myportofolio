from django.urls import path
from main.api_views import *

app_name = "api"

urlpatterns = [
    path("projects/", project_list, name="project_list"),
    path("projects/<uuid:project_id>/", project_detail, name="project_detail"),
    path("projects/<uuid:project_id>/star/", project_star, name="project_star"),
]