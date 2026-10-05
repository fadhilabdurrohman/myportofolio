from django.forms import ModelForm, TextInput, Textarea, NumberInput, URLInput, Select, DateInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from main.models import Skill, Project, Experience


# Skill form
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            'name',
            'icon',
            'url',
        ]

        labels = {
            'name': 'Name',
            'icon': 'Icon',
            'url': 'URL',
        }

        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Enter skill name',
                    'maxlength': 255,
                }
            ), 
            'icon': TextInput(
                attrs={
                    'placeholder': 'Enter icon filename',
                    'maxlength': 255,
                }
            ),
            'url': URLInput(
                attrs={
                    'placeholder': 'Enter skill URL',
                }
            )
        }

    def clean_name(self):
        name = strip_tags(self.cleaned_data["name"]).strip()

        if not name:
            raise ValidationError("Skill name cannot contain only HTML tags.")

        return name

    def clean_icon(self):
        icon = strip_tags(self.cleaned_data["icon"]).strip()

        if not icon:
            raise ValidationError("Icon filename cannot contain only HTML tags.")

        return icon


# Project form
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'year',
            'project_type',
            'url',
            'thumbnail',
        ]

        labels = {
            'title': 'Title',
            'description': 'Description',
            'year': 'Year',
            'project_type': 'Type',
            'url': 'URL',
            'thumbnail': 'Thumbnail',
        }

        widgets = {
            'title': TextInput(
                attrs={
                    'placeholder': 'Enter project title',
                    'maxlength': 255,
                }
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Enter project description',
                    'rows': 3,
                }
            ),
            'year': NumberInput(
                attrs={
                    'placeholder': 'Enter project year',
                    'min': 1900,
                    'max': 2100,
                }
            ),
            'project_type': TextInput(
                attrs={
                    'placeholder': 'Enter project type',
                    'maxlength': 255,
                }
            ),
            'url': URLInput(     
                attrs={
                    'placeholder': 'Enter project URL'
                }
            ),
            'thumbnail': URLInput(
                attrs={
                    'placeholder': 'Enter thumbnail URL'
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()

        if not title:
            raise ValidationError("Project title cannot contain only HTML tags.")

        return title

    def clean_project_type(self):
        project_type = strip_tags(self.cleaned_data["project_type"]).strip()

        if not project_type:
            raise ValidationError("Project type cannot contain only HTML tags.")

        return project_type

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()

        if not description:
            raise ValidationError("Project description cannot contain only HTML tags.")

        return description


# Experience form
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'title',
            'organization',
            'description',
            'category',
            'thumbnail',
            'started_at',
            'ended_at',
        ]

        labels = {
            'title': 'Title',
            'organization': 'Organization',
            'description': 'Description',
            'category': 'Category',
            'thumbnail': 'Thumbnail',
            'started_at': 'Start Date',
            'ended_at': 'End Date',
        }

        widgets = {
            'title': TextInput(
                attrs={
                    'placeholder': 'Enter experience title',
                    'maxlength': 255,
                }
            ),
            'organization': TextInput(
                attrs={
                    'placeholder': 'Enter organization name',
                    'maxlength': 255,
                }
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Enter experience description',
                    'rows': 3,
                }
            ),
            'category': Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'thumbnail': URLInput(
                attrs={
                    'placeholder': 'Enter thumbnail URL',
                }
            ),
            'started_at': DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'ended_at': DateInput(
                attrs={
                    'type': 'date',
                }
            )
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()

        if not title:
            raise ValidationError("Experience title cannot contain only HTML tags.")

        return title

    def clean_organization(self):
        organization = strip_tags(self.cleaned_data["organization"]).strip()

        if not organization:
            raise ValidationError("Organization cannot contain only HTML tags.")

        return organization

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()

        if not description:
            raise ValidationError("Experience description cannot contain only HTML tags.")

        return description
