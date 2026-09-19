from django.forms import ModelForm, TextInput, Textarea, NumberInput, URLInput, Select, DateInput

from main.models import Project, Experience

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
            'title': 'Nama Kegiatan',
            'organization': 'Penyelenggara Kegiatan',
            'description': 'Deskripsi Kegiatan',
            'category': 'Kategori Kegiatan',
            'thumbnail': 'Thumbnail Kegiatan',
            'started_at': 'Tanggal Mulai',
            'ended_at': 'Tanggal Selesai',
        }

        widgets = {
            'title': TextInput(
                attrs={
                    'placeholder': 'Staff of Academic',
                    'maxlength': 255,
                }
            ),
            'organization': TextInput(
                attrs={
                    'placeholder': 'Dasar-Dasar Pemrograman 0',
                    'maxlength': 255,
                }
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ceritakan Pengalamanmu',
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
                    'placeholder': 'https://drive.google.com/thumbnail',
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
