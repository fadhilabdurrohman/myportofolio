import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from main.models import Skill, Project, Experience

class ProjectAPITest(APITestCase):
    # Create test data
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.project = Project.objects.create(
            title="Portfolio",
            description="My website",
            year=2026,
            project_type="Django project",
        )

        self.list_url = reverse("api:project_list")
        self.detail_url = reverse("api:project_detail", args=[self.project.id])
        self.star_url = reverse("api:project_star", args=[self.project.id])

        self.payload = {
            "title": "ShareSpace",
            "description": "A sharing platform",
            "year": 2026,
            "project_type": "Django project",
            "url": "https://example.com/",
            "thumbnail": "",
        }

    # Test public list and detail
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertEqual(response.data[0]["year"], 2026)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)

    # Test search and empty results
    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})

        self.assertEqual(len(response.data), 1)

        response = self.client.get(self.list_url, {"title": "not-found"})

        self.assertEqual(response.data, [])

    # Test nonexistent project
    def test_missing_project(self):
        url = reverse("api:project_detail", args=[uuid.uuid4()])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # Test guest and visitor permissions
    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            response = self.client.post(self.list_url, self.payload, format="json")
            self.assertEqual(response.status_code, 403)

            response = self.client.put(self.detail_url, self.payload, format="json")
            self.assertEqual(response.status_code, 403)

            response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
            self.assertEqual(response.status_code, 403)

            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, 403)

        self.project.refresh_from_db()

        self.assertEqual(self.project.title, "Portfolio")
        self.assertEqual(Project.objects.count(), 1)

    # Test owner create permission and year conversion
    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {**self.payload, "year": "2026"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["year"], 2026)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    # Test invalid input
    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        invalid_values = [
            ("title", "   "),
            ("title", "<b></b>"),
            ("description", "<b></b>"),
            ("project_type", "<i></i>"),
            ("year", "wrong"),
            ("year", 1800),
            ("year", 2200),
            ("url", "javascript:alert(1)"),
            ("thumbnail", "invalid-url"),
        ]

        for field, value in invalid_values:
            with self.subTest(field=field, value=value):
                response = self.client.post(
                    self.list_url,
                    {**self.payload, field: value},
                    format="json",
                )

                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)

        self.assertEqual(Project.objects.count(), 1)

    # Test PATCH, PUT, and DELETE
    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")

        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()

        self.assertEqual(self.project.title, "Changed")
        self.assertEqual(self.project.description, "My website")

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")

        self.assertEqual(response.status_code, 400)

        response = self.client.put(self.detail_url, self.payload, format="json")

        self.assertEqual(response.status_code, 200)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    # Test star authentication and toggle
    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.visitor)

        for expected, count in [(True, 1), (False, 0)]:
            response = self.client.post(self.star_url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["is_starred"], expected)
            self.assertEqual(response.data["star_count"], count)
            self.assertEqual(self.project.starred_by.count(), count)

    # Test computed fields cannot be changed by client
    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    # Test staff and Editor permissions
    def test_staff_and_editor_permissions(self):
        self.visitor.is_staff = True
        self.visitor.save()

        self.client.force_authenticate(user=self.visitor)

        response = self.client.patch(self.detail_url, {"title": "Denied"}, format="json")

        self.assertEqual(response.status_code, 403)

        self.visitor.groups.add(Group.objects.create(name="Editor"))

        response = self.client.patch(self.detail_url, {"title": "Edited"}, format="json")

        self.assertEqual(response.status_code, 200)

        response = self.client.put(self.detail_url, self.payload, format="json")

        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, 403)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 403)

        self.project.refresh_from_db()

        self.assertEqual(self.project.title, "ShareSpace")

    # Test unsupported HTTP methods
    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.client.head(self.list_url).status_code, 200)
        self.assertEqual(self.client.options(self.list_url).status_code, 200)

    # Test session request without CSRF
    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(client.login(username="owner", password="test-password"))

        response = client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.count(), 1)

    # Test session request with CSRF
    def test_session_write_with_csrf_succeeds(self):
        test_cases = [
            ("owner", self.list_url, self.payload, 201),
            ("visitor", self.star_url, {}, 200),
        ]

        for username, endpoint, payload, expected in test_cases:
            client = APIClient(enforce_csrf_checks=True)

            self.assertTrue(client.login(username=username, password="test-password"))

            response = client.get(reverse("main:show_project"))

            self.assertEqual(response.status_code, 200)

            csrf_token = client.cookies["csrftoken"].value

            response = client.post(
                endpoint,
                payload,
                format="json",
                HTTP_X_CSRFTOKEN=csrf_token,
            )

            self.assertEqual(response.status_code, expected)

class SkillAPITest(APITestCase):
    # Create test data
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )
        self.editor.groups.add(Group.objects.create(name="Editor"))

        self.skill = Skill.objects.create(
            name="Python",
            icon="python.svg",
        )

        self.list_url = reverse("api:skill_list")
        self.detail_url = reverse("api:skill_detail", args=[self.skill.id])

        self.payload = {
            "name": "Django",
            "icon": "django.svg",
            "url": "https://www.djangoproject.com/",
        }

    # Test read access for each role
    def test_all_roles_can_read_list_and_detail(self):
        roles = (
            ("guest", None),
            ("visitor", self.visitor),
            ("editor", self.editor),
            ("owner", self.owner),
        )

        for role, user in roles:
            with self.subTest(role=role):
                self.client.force_authenticate(user=user)

                response = self.client.get(self.list_url)

                self.assertEqual(response.status_code, 200)
                self.assertEqual([item["id"] for item in response.data], [str(self.skill.id)])

                response = self.client.get(self.detail_url)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["id"], str(self.skill.id))

    # Test denied writes and verify database contents
    def test_guest_and_visitor_cannot_write(self):
        before = list(Skill.objects.order_by("pk").values())
        requests = (
            ("POST", self.client.post, self.list_url),
            ("PUT", self.client.put, self.detail_url),
            ("PATCH", self.client.patch, self.detail_url),
            ("DELETE", self.client.delete, self.detail_url),
        )

        for role, user in (("guest", None), ("visitor", self.visitor)):
            self.client.force_authenticate(user=user)

            for method, send, url in requests:
                with self.subTest(role=role, method=method):
                    response = send(url, self.payload, format="json")

                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(list(Skill.objects.order_by("pk").values()), before)

    # Test PUT and PATCH for Editor and owner
    def test_editor_and_owner_can_update(self):
        for role, user in (("editor", self.editor), ("owner", self.owner)):
            with self.subTest(role=role):
                self.client.force_authenticate(user=user)

                before = Skill.objects.values().get(pk=self.skill.id)
                patch_data = {"name": f"{role} PATCH"}
                response = self.client.patch(self.detail_url, patch_data, format="json")

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    Skill.objects.values().get(pk=self.skill.id),
                    {**before, **patch_data},
                )

                put_data = {**self.payload, "name": f"{role} PUT"}
                response = self.client.put(self.detail_url, put_data, format="json")

                self.assertEqual(response.status_code, 200)

                self.skill.refresh_from_db()

                self.assertEqual(self.skill.name, put_data["name"])

    # Test that Editor cannot add or remove records
    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        before = list(Skill.objects.order_by("pk").values())

        response = self.client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Skill.objects.order_by("pk").values()), before)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Skill.objects.order_by("pk").values()), before)

    # Test owner create and delete access
    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, 201)

        created = Skill.objects.get(pk=response.data["id"])

        self.assertNotEqual(created.id, self.skill.id)
        self.assertEqual(created.name, self.payload["name"])

        detail_url = reverse("api:skill_detail", args=[created.id])
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Skill.objects.filter(pk=created.id).exists())
        self.assertTrue(Skill.objects.filter(pk=self.skill.id).exists())


class ExperienceAPITest(APITestCase):
    # Create test data
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )
        self.editor.groups.add(Group.objects.create(name="Editor"))

        self.experience = Experience.objects.create(
            title="Teaching Assistant",
            organization="Universitas Indonesia",
            description="Helped students during lab sessions.",
            category="part-time",
            started_at="2026-01-01",
        )

        self.list_url = reverse("api:experience_list")
        self.detail_url = reverse("api:experience_detail", args=[self.experience.id])

        self.payload = {
            "title": "Research Assistant",
            "organization": "Universitas Indonesia",
            "description": "Prepared research data.",
            "category": "research",
            "thumbnail": "",
            "started_at": "2026-02-01",
            "ended_at": None,
        }

    # Test read access for each role
    def test_all_roles_can_read_list_and_detail(self):
        roles = (
            ("guest", None),
            ("visitor", self.visitor),
            ("editor", self.editor),
            ("owner", self.owner),
        )

        for role, user in roles:
            with self.subTest(role=role):
                self.client.force_authenticate(user=user)

                response = self.client.get(self.list_url)

                self.assertEqual(response.status_code, 200)
                self.assertEqual([item["id"] for item in response.data], [str(self.experience.id)])

                response = self.client.get(self.detail_url)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["id"], str(self.experience.id))

    # Test denied writes and verify database contents
    def test_guest_and_visitor_cannot_write(self):
        before = list(Experience.objects.order_by("pk").values())
        requests = (
            ("POST", self.client.post, self.list_url),
            ("PUT", self.client.put, self.detail_url),
            ("PATCH", self.client.patch, self.detail_url),
            ("DELETE", self.client.delete, self.detail_url),
        )

        for role, user in (("guest", None), ("visitor", self.visitor)):
            self.client.force_authenticate(user=user)

            for method, send, url in requests:
                with self.subTest(role=role, method=method):
                    response = send(url, self.payload, format="json")

                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(list(Experience.objects.order_by("pk").values()), before)

    # Test PUT and PATCH for Editor and owner
    def test_editor_and_owner_can_update(self):
        for role, user in (("editor", self.editor), ("owner", self.owner)):
            with self.subTest(role=role):
                self.client.force_authenticate(user=user)

                before = Experience.objects.values().get(pk=self.experience.id)
                patch_data = {"title": f"{role} PATCH"}
                response = self.client.patch(self.detail_url, patch_data, format="json")

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    Experience.objects.values().get(pk=self.experience.id),
                    {**before, **patch_data},
                )

                put_data = {**self.payload, "title": f"{role} PUT"}
                response = self.client.put(self.detail_url, put_data, format="json")

                self.assertEqual(response.status_code, 200)

                self.experience.refresh_from_db()

                self.assertEqual(self.experience.title, put_data["title"])

    # Test that Editor cannot add or remove records
    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        before = list(Experience.objects.order_by("pk").values())

        response = self.client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Experience.objects.order_by("pk").values()), before)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Experience.objects.order_by("pk").values()), before)

    # Test owner create and delete access
    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(self.list_url, self.payload, format="json")

        self.assertEqual(response.status_code, 201)

        created = Experience.objects.get(pk=response.data["id"])

        self.assertNotEqual(created.id, self.experience.id)
        self.assertEqual(created.title, self.payload["title"])

        detail_url = reverse("api:experience_detail", args=[created.id])
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=created.id).exists())
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

