from django.urls import path

from projects.views import *

app_name = 'projects'
urlpatterns = [
    path('', ProjectListView.as_view(), name='proyectos'),
    path('intereses/', ProjectListView.as_view(), name='proyectos-intereses'),
    path('intereses/<slug:category>/', ProjectInterestView.as_view(), name='proyectos-intereses-categoria'),
    path('intereses/<slug:category>/<slug:interest>/', ProjectInterestView.as_view(), name='proyectos-intereses-particular'),
    path('add-project/', add_project, name='add-project'),
    path('update-project/<slug>/', update_project, name='update-project'),
    path('delete-project/<slug>/', delete_project, name='delete-project'),
    path('project-add-tags/<slug:project_slug>/<slug:category>', ProjectAddTagView.as_view(), name='project-add-tags'),
    path('project-add-interest/<slug:project_slug>/<slug:tag>/', project_add_interest, name='project-add-interest'),
    path('project-delete-tags/<slug>', ProjectDeleteTagView.as_view(), name='project-delete-tags'),
    path('project-delete-interest/<slug:project_slug>/<slug:tag>/', project_delete_interest, name='project-delete-interest'),
    path('proyectos/filtro/', ProjectAdvancedFilterView.as_view(), name='project-filter'),
    path('delete-assignation/<slug>/', delete_assignation, name='delete-assignation'),
    path('join-project/<slug>/', join_project, name='join-project'),
    path('<slug>/', ProjectDetailView.as_view(), name='proyecto'),
    path('<slug>/miembros/', ProjectNewMembersView.as_view(), name='project-find-members'),
]
