from django.shortcuts import render
from main.models import Experience

# Create your views here.

def show_main(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "npm": "2506656690",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A learner intersted in science and technology"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fadhil Abdurrohman",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)