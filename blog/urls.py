from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^postlist/$', views.post_list, name='post_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),   
    url(r'^post/(?P<slug>[\w-]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<slug>[\w-]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<slug>[\w-]+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<slug>[\w-]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<slug>[\w-]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^about', views.about_page, name='about'),
       
]
