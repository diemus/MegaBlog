from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import View, ListView, CreateView, UpdateView
from blog.models import Post,Category
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
from django.views.generic.base import ContextMixin
from post_admin.models import SidebarNavItem
from django.views.decorators.csrf import csrf_exempt
from MegaBlog import settings
from PIL import Image
import datetime
import os
import uuid

class BaseMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['nav_list'] = SidebarNavItem.objects.filter(status=1).all()
        except Exception as e:
            print(e)
        return context

class LoginView(auth_views.LoginView):
    template_name = 'post_admin/login.html'

class LogoutView(auth_views.LogoutView):
    next_page = '/admin/login'

@method_decorator(login_required(login_url='/admin/login'), name='dispatch')
class PostsManagementView(BaseMixin,ListView):
    template_name = 'post_admin/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        post_list = Post.objects.filter(author_id=user.id).exclude(status=2)
        return post_list

@method_decorator(login_required(login_url='/admin/login'), name='dispatch')
class DeletePost(View):
    def get(self, request, *args, **kwargs):
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=request.user.id).get(pk=pkey)
        post.status = 2
        post.save()
        return redirect('/admin/')

@method_decorator(login_required(login_url='/admin/login'), name='dispatch')
class CreateNewPost(BaseMixin,CreateView):
    template_name = 'post_admin/post_edit.html'
    model = Post
    fields = ['title','content','category','tags','status','author']

    def get_context_data(self, **kwargs):
        context = super(CreateNewPost, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context

    def form_valid(self, form):
        # 覆盖原方法，验证后不保存
        pass

    def post(self, request, *args, **kwargs):
        # 先进行form验证
        super(CreateNewPost,self).post(request,*args, **kwargs)
        # 获取当前用户
        user = request.user
        # 获取文章内容
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        category = request.POST.get("category", "")
        tags = request.POST.getlist("tag", "")
        action = request.POST.get("action", "0")

        category_obj = Category.objects.get(name=category)

        post_obj = Post.objects.create(
            title=title,
            author=user,
            content=content,
            category=category_obj,
            status=action,
        )

        tag_list=tags[0].split(',')
        # 设置tags
        post_obj.update_tags(tag_list)

        return redirect('/admin')

@method_decorator(login_required(login_url='/admin/login'), name='dispatch')
class UpdatePost(BaseMixin,UpdateView):
    template_name = 'post_admin/post_edit.html'
    model = Post
    fields = ['title', 'content', 'category', 'tags', 'status', 'author']

    def get_context_data(self, **kwargs):
        context = super(UpdatePost, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context

    def form_valid(self, form):
        # 覆盖原方法，验证后不保存
        pass

    def post(self, request, *args, **kwargs):
        # 先进行form验证
        super(UpdatePost, self).post(request, *args, **kwargs)
        # 获取当前用户
        user = request.user
        # 获取要修改的文章ID
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=user.id).get(pk=pkey)
        # 获取其他内容
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        category = request.POST.get("category", "")
        tags = request.POST.getlist("tag", "")
        action = request.POST.get("action", "0")
        category_obj = Category.objects.get(name=category)

        post.title = title
        post.content = content
        post.category = category_obj
        post.status = action
        post.modify_time = datetime.datetime.now()
        post.save()

        tag_list = tags[0].split(',')
        # 设置tags
        post.update_tags(tag_list)

        return redirect('/admin')

@csrf_exempt
def tinymce_image_upload_handler(request):
    if request.method == "POST":
        try:
            file_img = request.FILES['tinymce-image-file']
            file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name)) - 1]
            # 检查图片格式
            if file_suffix not in settings.image_type:
                raise Exception("请上传正确格式的图片文件！")
            filename = uuid.uuid1().__str__() + file_suffix

            # 图片宽大于824的时候，将其压缩到824px，刚好适合13吋pc的大小
            img = Image.open(file_img)
            width, height = img.size
            if width > 824:
                img.thumbnail((width/(width/824.0),height/(width/824.0)))

            path = settings.MEDIA_ROOT + "/post/"
            if not os.path.exists(path):
                os.makedirs(path)

            file_name = path + filename
            img.save(file_name)

            file_img_url = "http://" + request.META['HTTP_HOST'] + settings.MEDIA_URL + "post/" + filename

            context = {
                'result': "file_uploaded",
                'resultcode': "ok",
                'file_name': file_img_url
            }

        except Exception as e:
            context = {
                'result': e,
                'resultcode': "failed",
            }
            print(e)

        return render(request, "post_admin/plugin/ajax_upload_result.html", context)

def avatar_image_upload_handler(request):
    if request.method == "POST":
        try:
            file_img = request.FILES['avatar']
            print(file_img)
            file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name)) - 1]
            # 检查图片格式
            if file_suffix.lower() not in settings.image_type:
                raise Exception("请上传正确格式的图片文件！")
            filename = uuid.uuid1().__str__() + file_suffix

            # 把头像压缩成90大小
            img = Image.open(file_img)
            img.thumbnail((90,90))

            path = settings.MEDIA_ROOT + "/avatar/"
            if not os.path.exists(path):
                os.makedirs(path)

            file_name = path + filename
            img.save(file_name)

            file_img_url = "http://" + request.META['HTTP_HOST'] + settings.MEDIA_URL + "avatar/" + filename
            user = request.user
            user.avatar_path = file_img_url
            user.save()

        except Exception as e:
            print(e)

        return redirect(request.META.get('HTTP_REFERER', "/"))

class PasswordChangeView(BaseMixin,auth_views.PasswordChangeView):
    success_url = '/admin/password_change/done'
    template_name = 'post_admin/password_change_form.html'

class PasswordChangeDoneView(BaseMixin,auth_views.PasswordChangeDoneView):
    template_name = 'post_admin/password_change_done.html'