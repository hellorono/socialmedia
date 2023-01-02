from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView

from socialweb.forms import UserRegistrationForm,LoginForm,PostForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from api.models import Posts
from django.utils.decorators import method_decorator
from django.contrib import messages


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"you must login first")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

class RegistrationView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    model=User
    success_url=reverse_lazy("signin")


    # def get(self,request,*args,**kw):
    #     form=UserRegistrationForm()
    #     return render(request,"register.html",{"form":form})
    
    # def post(self,request,*args,**kw):
    #     form=UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request,"your account created successfully")
    #         return redirect("signin")
    #     else:
    #         messages.error(request,"registration failed")
    #         return render(request,"register.html",{"form":form})

class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm

    # def get(self,request,*args,**kw):
    #     form=LoginForm()
    #     return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                messages.error(request,"invalid credentials")
                print("invalid")
                return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("home")
    context_object_name="posts"
    queryset=Posts.objects.all()

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user=self.request.user
            messages.success(self.request,"post created")
            return super().form_valid(form)
        else:
            return render(self.request,"index.html",{"form":form})
        

    def get_queryset(self):
        return Posts.objects.exclude(user=self.request.user).order_by("-created_date")
    # def get(self,request,*args,**kw):
    #     qs=Posts.objects.filter(user=request.user)
    #     return render(request,"post-list.html",{"posts":qs})

# @method_decorator(signin_required,name="dispatch")
# class PostCreateView(CreateView):
#     template_name="post-add.html"
#     form_class=PostForm
#     model=Posts
#     success_url=reverse_lazy("post-list")
    
    
    # def get(self,request,*args,**kw):
    #     form=PostForm()
    #     return render(request,"post-add.html",{"form":form})

    # def post(self,request,*args,**kw):
    #     form=PostForm(request.POST)
    #     if form.is_valid():
    #         instance=form.save(commit=False)
    #         instance.user=request.user
    #         instance.save()
    #         messages.success(request,"post created successfully")
    #         return redirect("post-list")
    #     else:
    #         messages.error(request,"failed to create post")
    #         return render(request,"post-add.html",{"form":form})

# @method_decorator(signin_required,name="dispatch")
# class PostDetailView(DetailView):
#     template_name="post-detail.html"
#     model=Posts
#     context_object_name="post"
#     pk_url_kwarg="id"
    # def get(self,request,*args,**kw):
    #     id=kw.get("id")
    #     qs=Posts.objects.get(id=id)
    #     return render(request,"post-detail.html",{"post":qs})

# @signin_required
# def post_delete_view(request,*args,**kw):
#     id=kw.get("id")
#     Posts.objects.get(id=id).delete()
#     messages.success(request,"post deleted successfully")
#     return redirect("post-list")

# @signin_required
# def sign_out_view(request,*args,**kw):
#     logout(request)
#     return redirect("signin")
def add_comment(request, *args, **kwargs):
        id = kwargs.get('id')
        cmt = request.POST.get('comment')
        qs = Posts.objects.get(id=id)
        qs.comments_set.create(user=request.user, comment=cmt)
        messages.success(request, "Comment added succesfully")
        return redirect("home")

def like_post(request, *args, **kwargs):
        id = kwargs.get('id')
        ps = Posts.objects.get(id=id)
        if ps.like.contains(request.user):
            ps.like.remove(request.user)
        else:
            ps.like.add(request.user)
        return redirect("home")

def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("signin")











