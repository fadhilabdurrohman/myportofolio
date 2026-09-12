import uuid
from django.db import models

# Create your models here.

class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    started_at = models.DateField(auto_now_add=True)
    ended_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.institution

    @property
    def is_ongoing(self):
        return self.ended_at is None

    @property
    def date_range(self):
        start = self.started_at.strftime("%Y")

        if self.ended_at is None:
            return f"{start} - Present"

        end = self.ended_at.strftime("%Y")
        return f"{start} - {end}"

class Skills(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_lenght=True)
    icon = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    url = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField(auto_now_add=True)
    ended_at = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

    @property
    def date_range(self):
        start = self.started_at.strftime("%b %Y")

        if self.ended_at is None:
            return f"{start} - Present"

        end = self.ended_at.strftime("%b %Y")
        return f"{start} - {end}"
