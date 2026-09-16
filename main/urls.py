from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("skill/", show_skill, name="show_skill"),
    path("project/", show_project, name="show_project"),
    path("experience/", show_experience, name="show_experience"),
    path("project/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("project/<uuid:project_id>/delete/",delete_project,name="delete_project")
]
