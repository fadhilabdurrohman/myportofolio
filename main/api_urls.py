from django.urls import path
from main.api_views import *

app_name = "api"

urlpatterns = [
    path("projects/", project_list, name="project_list"),
    path("projects/<uuid:project_id>/", project_detail, name="project_detail"),
    path("projects/<uuid:project_id>/star/", project_star, name="project_star"),
    path("skills/", skill_list, name="skill_list"),
    path("skills/<uuid:skill_id>/", skill_detail, name="skill_detail"),
    path("experiences/", experience_list, name="experience_list"),
    path("experiences/<uuid:experience_id>/", experience_detail, name="experience_detail"),
]
