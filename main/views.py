from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied        
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from django.views.decorators.http import require_POST
from main.models import *
from main.forms import SkillForm, ProjectForm, ExperienceForm
import datetime

# Create your views here.

# Display the main page
def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)

# Display the skill page
def show_skill(request):
    name_query = request.GET.get("name", "").strip()

    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "name_query": name_query,
        "form": SkillForm(),
        "is_editor": is_editor(request.user),
    }

    return render(request, "skill.html", context)

# Display the project page
def show_project(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "title_query": title_query,
        "form": ProjectForm(),
        "is_editor": is_editor(request.user),
    }
    return render(request, "project.html", context)

# Display the experience page
def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Fadhil Abdurrohman",
        "nickname": "Fadhil",
        "title_query": title_query,
        "form": ExperienceForm(),
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)

# Create skill
@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

# JSON skill
# JSON skill
def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.prefetch_related("starred_by").all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for skill in skills:
        starred_users = skill.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(skill.id),
            "fields": {
                "name": skill.name,
                "url": skill.url,
                "icon": skill.icon,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

# Delete skill
@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")

# Update skill
@login_required(login_url="/login/")
def update_skill(request, skill_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Editor").exists():
        raise PermissionDenied
    
    skill = get_object_or_404(Skill, pk=skill_id)

    form = SkillForm(
        request.POST or None,
        instance=skill
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skill")

    context = {
        "name": "Fadhil",
        "form": form,
        "skill": skill,
    }

    return render(request, "skill_form.html", context)

# Create project
@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

# JSON project
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "year": project.year,
                "project_type": project.project_type,
                "url": project.url,
                "thumbnail": project.thumbnail,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

# Delete project
@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

# Update project
@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Editor").exists():
            raise PermissionDenied
    
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

# Create experience
@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

# JSON experience
# JSON experience
def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "organization": experience.organization,
                "description": experience.description,
                "category": experience.category,
                "started_at": experience.started_at,
                "ended_at": experience.ended_at,
                "thumbnail": experience.thumbnail,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

# Delete experience
@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

# Update experience
@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Editor").exists():
        raise PermissionDenied
    
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

# Register
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account crated successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Fadhil",
        "form": form,
    }
    return render(request, "register.html", context)

# Login
def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Fadhil",
        "form": form,
    }
    return render(request, "login.html", context)

# Logout
def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Skill star
@login_required(login_url="/login/")
def toggle_skill_star(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
        else:
            skill.starred_by.add(request.user)

    return redirect("main:show_skill")

# Project star
@login_required(login_url="/login/")
def toggle_project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")

# Experience star
@login_required(login_url="/login/")
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
