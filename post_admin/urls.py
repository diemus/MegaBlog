from django.conf.urls import url, include
from django.contrib import admin
from blog import views
from blog.views import IndexView, TagListView, CategoryListView, SearchView, PostView
# CommentView,CommentDeleteView,
from post_admin.views import PostsManagementView, LoginView, LogoutView, DeletePost, CreateNewPost, UpdatePost, \
    tinymce_image_upload_handler,avatar_image_upload_handler,PasswordChangeView,PasswordChangeDoneView

urlpatterns = [
    url(r'^$', PostsManagementView.as_view()),
    url(r'^login', LoginView.as_view()),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^delete/(?P<pk>[0-9]+)$', DeletePost.as_view()),
    url(r'^new$', CreateNewPost.as_view()),
    url(r'^add$', CreateNewPost.as_view()),
    url(r'^update/draft/(?P<pk>[0-9]+)$', UpdatePost.as_view()),
    url(r'^update/post/(?P<pk>[0-9]+)$', UpdatePost.as_view()),
    url(r'^update/(?P<pk>[0-9]+)$', UpdatePost.as_view()),
    url(r'^upload/tinymce/post$', tinymce_image_upload_handler),
    url(r'^set/upload/avatar$', avatar_image_upload_handler),
    url(r'^password_change/$', PasswordChangeView.as_view()),
    url(r'^password_change/done$', PasswordChangeDoneView.as_view()),
]
