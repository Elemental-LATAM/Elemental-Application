from django.urls import path

from members.views import *

app_name = 'members'
urlpatterns = [
    path('miembros/', MemberListView.as_view(), name='miembros'),
    path('miembros/skills/', MemberSkillView.as_view(), name='miembros-skills'),
    path('miembros/skills/<slug:category>/', MemberSkillView.as_view(), name='miembros-skills-categoria'),
    path('miembros/skills/<slug:category>/<slug:skill>', MemberSkillView.as_view(), name='miembros-skills-particular'),
    path('miembros/intereses/', MemberInterestView.as_view(), name='miembros-intereses'),
    path('miembros/intereses/<slug:category>/', MemberInterestView.as_view(), name='miembros-intereses-categoria'),
    path('miembros/intereses/<slug:category>/<slug:interest>', MemberInterestView.as_view(), name='miembros-intereses-particular'),
    path('miembros/filtro/', MemberAdvancedFilterView.as_view(), name='member-filter'),
    path('miembro/<slug>/', MemberDetailView.as_view(), name='miembro'),
    path('add-tags/<slug:designation>/<slug:category>', MemberAddTagView.as_view(), name='add-tags'),
    path('delete-tags/', MemberDeleteTagView.as_view(), name='delete-tags'),
    path('add-skill/<slug:tag>/', add_skill, name='add-skill'),
    path('delete-interest/<slug:tag>', delete_interest, name='delete-interest'),
    path('add-interest/<slug:tag>/', add_interest, name='add-interest'),
    path('delete-skill/<slug:tag>', delete_skill, name='delete-skill'),
    path('update-user/', update_user, name='update-user'),
    path('getSkills/',  get_skill_for_register, name='get_skill_for_register'),
    path('getInterest/', get_interest_for_register, name='get_skill_for_register'),
]
