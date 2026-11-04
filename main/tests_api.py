import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from main.models import Project

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