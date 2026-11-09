from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Skill, Project, Experience

class ProjectSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(min_value=1900, max_value=2100)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "title", "description", "year", "project_type", "url", "thumbnail", "star_count", "is_starred", "starred_by_names"]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Title cannot be empty.")

        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Description cannot be empty.")

        return value

    def validate_project_type(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Project type cannot be empty.")

        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

# Skill serializer
class SkillSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "icon",
            "url",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_name(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Skill name cannot be empty.")

        return value

    def validate_icon(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Icon filename cannot be empty.")

        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

# Experience serializer
class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "organization",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Title cannot be empty.")

        return value

    def validate_organization(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Organization cannot be empty.")

        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError("Description cannot be empty.")

        return value

    def validate(self, attrs):
        started_at = attrs.get(
            "started_at",
            getattr(self.instance, "started_at", None),
        )
        ended_at = attrs.get(
            "ended_at",
            getattr(self.instance, "ended_at", None),
        )

        if (
            started_at is not None
            and ended_at is not None
            and ended_at < started_at
        ):
            raise serializers.ValidationError({
                "ended_at": "End date cannot be earlier than start date.",
            })

        return attrs

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
