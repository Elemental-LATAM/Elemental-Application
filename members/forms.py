from django.forms import ModelForm
from .models import Member


class MemberFileForm(ModelForm):
    class Meta:
        model = Member
        fields = ['image', 'resume']
