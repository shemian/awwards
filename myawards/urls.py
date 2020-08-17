from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views


urlpatterns=[
    url(r'^$',views.index,name = 'index'),
    url(r'profile/', views.profile, name='profile'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^project/(?P<project_id>.*)/$',views.project,name ='project'),
    url(r'^post/', views.upload_form, name='post'),
    url(r'^api/events/$', views.EventList.as_view()),
    url(r'api/events/event-id/(?P<pk>[0-9]+)/$',
        views.EventDescription.as_view()),
    url(r'^api/profiles/$', views.ProfileList.as_view()),
    url(r'api/profiles/profile-id/(?P<pk>[0-9]+)/$',
        views.ProfileDescription.as_view()),
    url(r'^api/projects/$', views.ProjectsList.as_view()),
    url(r'api/projects/project-id/(?P<pk>[0-9]+)/$',
        views.ProjectsDescription.as_view()),   
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)