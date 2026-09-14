from django.shortcuts import render
from django.db.models import F
from main.models import *

# Create your views here.

# Display the main page
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
        "education_list": Education.objects.all().order_by(F('ended_at').desc(nulls_first=True)),
    }
    return render(request, "index.html", context)

# Display the skill page
def show_skill(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "skill_list": Skill.objects.all().order_by('name'),
    }
    return render(request, "skill.html", context)

# Display the project page
def show_project(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "project_list": Project.objects.all().order_by('year'),
    }
    return render(request, "project.html", context)

# Display the experience page
def show_experience(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "experience_list": Experience.objects.all().order_by(F('ended_at').desc(nulls_first=True)),
    }
    return render(request, "experience.html", context)
