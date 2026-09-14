from django.test import TestCase
from django.urls import reverse
from datetime import date

from main.models import *


class MainTest(TestCase):
    # Create test data for each model
    def setUp(self):
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            program="Computer Science",
            started_at=date(2025, 8, 25),
            ended_at=None,
        )

        self.skill = Skill.objects.create(
            name="Python",
            icon="python.svg",
            url="https://www.python.org/",
        )

        self.project = Project.objects.create(
            title="Portofolio Website",
            description="A personal portfolio website developed with Django to showcase my projects, experiences, and technical skills. The website features a clean and responsive design with structured sections for presenting my background, experience, projects, and skills.",
            year=2026,
            project_type="Django project",
        )
        
        self.experience = Experience.objects.create(
            title="Teaching Asistant for Introduction to Computer Organization",
            description="Supported practical sessions by supervising and grading studentwork, developed assignments and practical exercises, and proctored examinations.",
            category="part-time",
            started_at=date(2026, 7, 22),
            ended_at=None,
        )

    # Test main page accessibility and navigation
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    # Test that nonexistent pages return 404
    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    # Test Experience model fields and ongoing status
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Teaching Asistant for Introduction to Computer Organization")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    # Test experience page content
    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Jul 2026 - Present")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    # Test experience page when no data exists
    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience added yet.")

    # Test Project model fields
    def test_project_model(self):
        self.assertEqual(str(self.project), "Portofolio Website")
        self.assertEqual(self.project.year, 2026)
        self.assertEqual(self.project.project_type, "Django project")

    # Test project page content
    def test_project_page(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "2026")
        self.assertContains(response, "Django project")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    # Test displaying multiple projects
    def test_multiple_projects(self):
        my_project = Project.objects.create(
            title="BurhanQuest",
            description="A Java-based terminal game developed using object-oriented programming.",
            year=2026,
            project_type="Java project",
        )
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, my_project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, my_project.description)

    # Test project page when no data exists
    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No project added yet.")

    # Test Skill model fields
    def test_skill_model(self):
        self.assertEqual(str(self.skill), "Python")
        self.assertEqual(self.skill.name, "Python")
        self.assertEqual(self.skill.icon, "python.svg")
        self.assertEqual(self.skill.url, "https://www.python.org/")

    # Test skill page content
    def test_skill_page(self):
        response = self.client.get(reverse("main:show_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        self.assertContains(response, self.skill.name)
        self.assertContains(response, self.skill.icon)
        self.assertContains(response, self.skill.url)

    # Test displaying multiple skills
    def test_multiple_skills(self):
        my_skill = Skill.objects.create(
            name="Java",
            icon="java.svg",
            url="https://www.java.com/",
        )
        response = self.client.get(reverse("main:show_skill"))

        self.assertContains(response, self.skill.name)
        self.assertContains(response, my_skill.name)
        self.assertContains(response, self.skill.icon)
        self.assertContains(response, my_skill.icon)

    # Test skill page when no data exists
    def test_empty_skill_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No skill added yet.")

    # Test Education model fields and date range
    def test_education_model(self):
        self.assertEqual(str(self.education), "Universitas Indonesia")
        self.assertEqual(self.education.institution, "Universitas Indonesia")
        self.assertEqual(self.education.program, "Computer Science")
        self.assertTrue(self.education.is_ongoing)
        self.assertEqual(self.education.date_range, "2025 - Present")

    # Test education content on the main page
    def test_education_page(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.program)
        self.assertContains(response, self.education.date_range)
