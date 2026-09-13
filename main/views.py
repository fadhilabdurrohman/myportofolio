from django.shortcuts import render
from main.models import *

# Create your views here.

def show_main(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "npm": "2506656690",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A learner intersted in science and technology"
        ),
        "about": (
            "I am a second year Computer Science student and a Teaching Assistant at Universitas Indonesia. I love learning " 
            "new things, especially anything related to sciences, mathematics, and technologies. Beyond that, I also enjoy "
            "exploring other subjects like culture and philosophy. I like playing chess, even though I'm not very good at it :)"
        ),
        "education_list": Education.objects.all(),
    }
    return render(request, "index.html", context)

def show_skill(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skill.html", context)

def show_project(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "project_list": Project.objects.all(),
    }
    return render(request, "project.html", context)

def show_experience(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
