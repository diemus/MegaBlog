"""MegaBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import views
from blog.views import IndexView,  TagListView, CategoryListView, SearchView,PostView,CommentView,CommentDeleteView
#CommentView,CommentDeleteView,
from post_admin import urls as admin_urls
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(admin_urls)),
    url(r'^$', IndexView.as_view()),
    url(r'^post/(?P<pk>[0-9]+)$', PostView.as_view()),
    url(r'^comment/add/(?P<pk>[0-9]+)$', CommentView.as_view()),
    url(r'^comment/delete/(?P<pk>[0-9]+)$', CommentDeleteView.as_view()),
    url(r'^tag/(?P<slug>[\w\u4e00-\u9fa5]+)$', TagListView.as_view(),name='tag'),
    url(r'^category/(?P<slug>[\w\u4e00-\u9fa5]+)$', CategoryListView.as_view(),name='category'),
    url(r'^search$', SearchView.as_view()),

]
