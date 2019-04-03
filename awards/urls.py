from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    
    url('^$',views.index, name='index'),
    url(r'^$',views.profile,name = 'profile'),
    url(r'^profile/', views.profile, name='profile'),
     url(r'^upload/profile', views.upload_profile, name='upload_profile'),
     url(r'^upload/', views.send, name='upload'),
     url(r'^search/', views.search_results, name='search_results'),


]
if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)