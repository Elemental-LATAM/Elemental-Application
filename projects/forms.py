from django.forms import ModelForm
from .models import Project


class ProjectFileForm(ModelForm):
    class Meta:
        model = Project
        fields = ['image']
