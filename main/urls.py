from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("skill/", show_skill, name="show_skill"),
    path("project/", show_project, name="show_project"),
    path("experience/", show_experience, name="show_experience"),
    path("skill/add/", create_skill, name="create_skill"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skill/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("project/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("project/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("project/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
]
