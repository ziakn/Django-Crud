"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from blog import views

app_name = "blog"

urlpatterns = [
    url(r'(?P<id>\d+)/post_edit/$', views.post_edit, name="post_edit"),
    url(r'(?P<id>\d+)/post_delete/$', views.post_delete, name="post_delete"),
    url(r'(?P<id>\d+)/delete_save_data/$', views.delete_save_data, name="delete_save_data"),
    url(r'(?P<id>\d+)/edit_save_data/$', views.edit_save_data, name="edit_save_data"),
    url(r'(?P<id>\d+)/(?P<slug>[\w-]+)/post_detail/$', views.post_detail, name="post_detail"),

    url(r'post_create/$', views.post_create, name="post_create"),
    url(r'edit_profile/$', views.edit_profile, name="edit_profile"),

    url(r'save_data/$', views.save_data, name="save_data"),


]
