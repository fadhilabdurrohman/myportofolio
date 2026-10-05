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
    path("skill/<uuid:skill_id>/edit/", update_skill, name="update_skill"),
    path("project/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("project/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("project/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experiences/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("skill/<uuid:skill_id>/star/", toggle_skill_star, name="toggle_skill_star"),
    path("project/<uuid:project_id>/star/", toggle_project_star, name="toggle_project_star"),
    path("experience/<uuid:experience_id>/star/", toggle_experience_star, name="toggle_experience_star"),
    path("skill/add-ajax/", create_skill_ajax, name="create_skill_ajax"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path("skill/<uuid:skill_id>/star-ajax/", toggle_skill_star_ajax, name="toggle_skill_star_ajax"),
    path("project/<uuid:project_id>/star-ajax/", toggle_project_star_ajax, name="toggle_project_star_ajax"),
    path("experience/<uuid:experience_id>/star-ajax/", toggle_experience_star_ajax, name="toggle_experience_star_ajax"),
    path("skill/<uuid:skill_id>/delete-ajax/", delete_skill_ajax, name="delete_skill_ajax"),
    path("project/<uuid:project_id>/delete-ajax/", delete_project_ajax, name="delete_project_ajax"),
    path("experience/<uuid:experience_id>/delete-ajax/", delete_experience_ajax, name="delete_experience_ajax"),
]
