from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from core.aux import validate_file_size
from core.models import Interest, Skill, InterestCategory, SkillCategory


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField("date created", auto_now_add=True)
    summary = models.CharField(max_length=140, blank=True)
    description = models.TextField(blank=True)
    linkedin = models.CharField(max_length=256, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to="img/people", blank=True, validators=[validate_file_size])
    resume = models.FileField(upload_to="docs/resume", blank=True, validators=[validate_file_size])

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("members:miembro", kwargs={
            'slug': self.slug
        })


class MemberInterest(models.Model):
    slug = models.IntegerField(unique=True)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    category_slug = models.CharField(max_length=30, default='')
    interest_slug = models.CharField(max_length=30, default='')

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return str(self.member.name) + "-" + str(self.interest.name)

    def get_delete_url(self):
        return reverse("members:delete-interest", kwargs={
            'tag': self.slug,
        })

    def get_tag_name(self):
        return self.interest.name


class MemberInterestCategory(models.Model):
    slug = models.IntegerField(unique=True)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return str(self.member.name) + "-" + str(self.category.name)


class MemberSkill(models.Model):
    slug = models.IntegerField(unique=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    category_slug = models.CharField(max_length=30, default='')
    skill_slug = models.CharField(max_length=30, default='')

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return str(self.member.name) + "-" + str(self.skill.name)

    def get_delete_url(self):
        return reverse("members:delete-skill", kwargs={
            'tag': self.slug,
        })

    def get_tag_name(self):
        return self.skill.name


class MemberSkillCategory(models.Model):
    slug = models.IntegerField(unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return str(self.member.name) + "-" + str(self.category.name)


