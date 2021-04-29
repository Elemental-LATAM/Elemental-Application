from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
import datetime

from core.aux import validate_file_size
from core.models import Interest, InterestCategory, Skill, SkillCategory


class Project(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField("date created", auto_now_add=True)
    project_date = models.DateTimeField("since", blank=True, default=datetime.date.today)
    summary = models.CharField(max_length=140)
    description = models.TextField()
    status = models.CharField(max_length=140, default="En desarrollo")
    active = models.BooleanField(default=True)
    description_candidate = models.CharField(max_length=256, default="")
    timeline = models.CharField(max_length=2048, default="[]")
    image = models.ImageField(upload_to="img/projects", blank=True, validators=[validate_file_size])

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:proyecto", kwargs={
            'slug': self.slug
        })

    def get_update_project_url(self):
        return reverse("projects:update-project", kwargs={
            'slug': self.slug
        })

    def get_delete_project_url(self):
        return reverse("projects:delete-project", kwargs={
            'slug': self.slug
        })

    def get_join_project_url(self):
        return reverse("projects:join-project", kwargs={
            'slug': self.slug
        })


class ProjectInterest(models.Model):
    slug = models.IntegerField(unique=True)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category_slug = models.CharField(max_length=30, default='')
    interest_slug = models.CharField(max_length=30, default='')

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return str(self.project.title) + "-" + str(self.interest.name)

    def get_delete_url(self):
        return reverse("projects:project-delete-interest", kwargs={
            'project_slug': self.project.slug,
            'tag': self.slug,
        })

    def get_tag_name(self):
        return self.interest.name


class ProjectInterestCategory(models.Model):
    slug = models.IntegerField(unique=True)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return str(self.project.title) + "-" + str(self.category.name)


class Assignation(models.Model):
    slug = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.user.username + "-" + self.project.title

    def get_delete_assignation_url(self):
        return reverse("projects:delete-assignation", kwargs={
            'slug': self.slug
        })
