from django.forms import ModelForm, TextInput, Textarea, NumberInput, URLInput

from main.models import Project

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
            'title': 'Nama Proyek',
            'description': 'Deskripsi Proyek',
            'year': 'Tahun Proyek',
            'project_type': 'Tipe Proyek',
            'url': 'URL Proyek',
            'thumbnail': 'Thumbnail Proyek',
        }

        widgets = {
            'title': TextInput(
                attrs={
                    'placeholder': 'Potofolio Website',
                    'maxlength': 255,
                }
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ceritakan Proyekmu',
                    'rows': 3,
                }
            ),
            'year': NumberInput(
                attrs={
                    'placeholder': '2026',
                    'min': 1900,
                    'max': 2100,
                }
            ),
            'project_type': TextInput(
                attrs={
                    'placeholder': 'Django Project',
                    'maxlength': 255,
                }
            ),
            'url': URLInput(
                attrs={
                    'placeholder': 'https://github.com/Burhan/BurhanQuest'
                }
            ),
            'thumbnail': URLInput(
                attrs={
                    'placeholder': 'https://drive.google.com/thumbnail'
                }
            ),
        }
