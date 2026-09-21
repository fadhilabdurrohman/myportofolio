from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from main.models import *
from main.forms import SkillForm, ProjectForm, ExperienceForm

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
    json_response = get_skills_json(request)
    
    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [skill.object for skill in skills]
    title_query = request.GET.get("name", "").strip()

    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "skill_list": skills,
        "title_query": title_query,
    }

    return render(request, "skill.html", context)

# Display the project page
def show_project(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "project.html", context)

# Display the experience page
def show_experience(request):
    json_response = get_experience_json(request)
    
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skill")

    context = {
        "name": "Fadhil",
        "form": form,
    }
    return render(request, "skill_form.html", context)

def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Fadhil",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    form = ProjectForm(
        request.POST or None,
        instance=project
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_project")

    context = {
        "name": "Fadhil",
        "form": form,
        "project": project,
    }

    return render(request, "projects_form.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
            "name": "Fadhil",
            "form": form,
        }
    return render(request, "experience_form.html", context)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Fadhil",
        "form": form,
        "experience": experience,
    }

    return render(request, "experience_form.html", context)
