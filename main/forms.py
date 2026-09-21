from django.forms import ModelForm, TextInput, Textarea, NumberInput, URLInput, Select, DateInput

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
