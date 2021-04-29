from django.db import models
from django.urls import reverse


class SkillCategory(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(unique=True, max_length=30)
    quantity = models.IntegerField(default=0)
    top = models.BooleanField(default=False)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.name

    def get_member_category_url(self):
        return reverse("members:miembros-skills-categoria", kwargs={
            'category': self.slug
        })

    def get_tags_url(self):
        return reverse("members:add-tags", kwargs={
            'designation': 'skills',
            'category': self.slug,
        })


class InterestCategory(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(unique=True, max_length=30)
    quantity = models.IntegerField(default=0)
    top = models.BooleanField(default=False)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.name

    def get_project_category_url(self):
        return reverse("projects:proyectos-intereses-categoria", kwargs={
            'category': self.slug
        })

    def get_member_category_url(self):
        return reverse("members:miembros-intereses-categoria", kwargs={
            'category': self.slug
        })

    def get_tags_url(self):
        return reverse("members:add-tags", kwargs={
            'designation': 'intereses',
            'category': self.slug,
        })


class Skill(models.Model):
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=30)
    quantity = models.IntegerField(default=0)
    top_category = models.BooleanField(default=False)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.name

    def get_member_interest_url(self):
        category_slug = self.category.slug
        return reverse("members:miembros-skills-particular", kwargs={
            'category': category_slug,
            'skill': self.slug
        })

    def add_tag(self):
        return reverse("members:add-skill", kwargs={
            'tag': self.slug,
        })


class Interest(models.Model):
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=30)
    quantity = models.IntegerField(default=0)
    top_category = models.BooleanField(default=False)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.name

    def get_project_interest_url(self):
        category_slug = self.category.slug
        return reverse("projects:proyectos-intereses-particular", kwargs={
            'category': category_slug,
            'interest': self.slug
        })

    def get_member_interest_url(self):
        category_slug = self.category.slug
        return reverse("members:miembros-intereses-particular", kwargs={
            'category': category_slug,
            'interest': self.slug
        })

    def add_tag(self):
        return reverse("members:add-interest", kwargs={
            'tag': self.slug,
        })

